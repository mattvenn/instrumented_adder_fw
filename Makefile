
TOOLCHAIN_PATH=/opt/riscv64-unknown-elf-gcc-8.3.0-2020.04.1-x86_64-linux-ubuntu14/bin/
#TOOLCHAIN_PATH=/usr/local/bin/
#TOOLCHAIN_PATH=/opt/riscv32imc/bin/
# TOOLCHAIN_PATH=/ef/apps/bin/

# Set the prefix for `riscvXX-unknown-elf-*`
# On installations using `multilib`, this will be `riscv64` even for compiling to 32-bit targets
TOOLCHAIN_PREFIX=riscv64-unknown-elf
#TOOLCHAIN_PREFIX=riscv32

# ---- Test patterns for project raven ----

.SUFFIXES:

PATTERN = adder

hex:  ${PATTERN:=.hex}

%.elf: %.c ../sections.lds ../crt0_vex.S
	#$(TOOLCHAIN_PATH)riscv32-unknown-elf-gcc -O0 -march=rv32i -Wl,-Bstatic,-T,../sections.lds,--strip-debug -ffreestanding -nostdlib -o $@ ../start.s ../print_io.c $<
	$(TOOLCHAIN_PATH)$(TOOLCHAIN_PREFIX)-gcc -I../ -I../generated/ -O0 -mabi=ilp32 -march=rv32i -D__vexriscv__ -Wl,-Bstatic,-T,../sections.lds,--strip-debug -ffreestanding -nostdlib -o $@ ../crt0_vex.S ../isr.c ../stub.c $<
	${TOOLCHAIN_PATH}$(TOOLCHAIN_PREFIX)-objdump -D adder.elf > adder.lst

%.hex: %.elf
	$(TOOLCHAIN_PATH)$(TOOLCHAIN_PREFIX)-objcopy -O verilog $< $@
	sed -ie 's/@1000/@0000/g' $@

%.bin: %.elf
	$(TOOLCHAIN_PATH)$(TOOLCHAIN_PREFIX)-objcopy -O binary $< $@

client: client.c
	gcc client.c -o client

flash: adder.hex
	python3 ../util/caravel_hkflash.py adder.hex

flash2: adder.hex
	python3 ../util/caravel_flash.py adder.hex

# ---- Clean ----

clean:
	rm -f *.elf *.hex *.bin *.vvp *.vcd

monitor:
#	pio device monitor -p /dev/serial/by-id/usb-Arduino_Nano_33_BLE_3C48BB3E0BD44A03-if00 -b 9600
	pio device monitor -p /dev/serial/by-id/usb-Arduino_LLC_Arduino_Leonardo-if00  -b 9600


.PHONY: clean hex all flash

