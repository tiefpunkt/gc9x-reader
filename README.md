# GC9x DC power meter TTL readout

The GC90 power meter can measure DC power up to 200V and 20A. It has a TTL port (inside a Micro USB connector). There's also a variant for higher currents, using and external shunt, called GC91.

## Protocol
* Baud rate: 19200
* check digit: NONE data bits: 8 stop bits: 1

### Sending Instructions
All instructions start with 7733 marks.
1. Clear current power-on capacity, load time and watt-hour to the equipment.
  * Practical example: 77 33 C0 02
  * Number correspondence: 01 02 03 04
    * 01 02: Identification Header
    * 03: Device Address+0xC0
    * 04: This Record Zero-clearing Instruction Code
2. Clearing cumulative-capacity, load-carrying time, watt-hour to equipment:
  * Practical example: 77 33 C0 03
  * Number correspondence: 01 02 03 04
    * 01 02: Identification Header
    * 03: Device Address+0xC0
    * 04: Cumulative Record Zero Clearing Instruction Code
3. To issue instructions to the device to change the data output mode:
  * Practical example: 77 33 C0 41
  * Number correspondence: 01 02 03 04
    * 01 02: Identification Header
    * 03: Device Address+0xC0
    * 04: Instruction Code
      * 40 - Stop Output
      * 41 - Output a set of data
      * 42 - Start Continuous Output Data
      * Outgoing by default is 40
4. Issue instructions to fix the address of the equipment:
  * Practical example: 77 33 C0 81
  * Number correspondence: 01 02 03 04
    * 01 02: Identification Header
    * 03: Device Address+0xC0
    * 04: Instruction Code
      * New Address = 0x81-0x80
      * Address Range 0x00-0x7f Total 128 So Instruction Code Range is 0x80-0xff
5. To issue mandatory instructions to the equipment:
  * Practical example: 77 33 8A
  * Number correspondence: 01 02 03
    * 01 02: Identification Header
    * 03: Instruction Code
      * 8A - Unconditional Stop Output
      * 8B - Unconditional Single Output Set of Data
  * This command ignores the device address and can be used to view the device address when it is forgotten that the device address cannot be controlled.
### Output
* Each output will output a set of device information consisting of 44 bytes.
* A single output can be triggered by sending the 77 33 C0 41 to the device
* The instrument outputs a set of information every time. It can filter and select useful information according to needs.

Practical example: FE FE FE FE 00 00 00 FD E8 00 00 3F 48 00 10 11 48 00 01 2B 5A 00 00 00 04 00 00
                               04 9A 00 02 3C 5B 00 00 05 9B 00 00 00 0B 01 26 00
Order sequence: 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44
* 01 - 04: FEFE FEFE data group start sign
* 05 : the local device address, defaults to 0.
* 06 - 09: Voltage. Format: Unsigned long, MSB. Unit: mV.
* 10 - 13: Current. Format: Unsigned long, MSB. Unit: mA.
* 14 - 17: Power. Format: Unsigned long, MSB. Unit: mW.
* 18 - 21: Power usage. Format: Unsigned long, MSB. Unit: mWH.
* 22 - 25: Load time Format: Unsigned long, MSB. Unit: minutes.
* 26 - 29: Capacity. Format: Unsigned long, MSB. Unit: mAH.
* 30 - 33: Cumulative power usage. Format: Unsigned long, MSB. Unit: mWH.
* 34 - 37: Cumulative capacity. Format: Unsigned long, MSB. Unit: mAH.
* 38 - 41: Cumulative load time. Format: Unsigned long, MSB. Unit: minutes.
* 42 - 43: Temperature. Format: Unsigned int, MSB. Unit: 0.1 degrees.
* 44: the current control level output state 0 is low level 1 is high level.
