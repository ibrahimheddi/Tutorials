# FPGA #
 
## 1 INTRODUCTION ## 
The protocol that we will use is called Serial Peripheral Interface (SPI)  commonly used to send data between microcontrollers and small peripherals such as shift registers,EEPROM, FLASH memory, A/D converters, temperature sensors, or in our case a Field Programmable Gate Array (FPGA).
We will program with  the VHDL  hardware description language.
if you are not able to program  with this language you can use this link to  start : https://tcuvelier.developpez.com/tutoriels/vhdl/introduction-langage/



## 2 HARDWARE ## 
SPI is a protocol, in which one device (the master) controls one or more other devices (the slaves). For the master we use an open-source microcontroller prototyping platform, like  Arduino UNO R3.
The slave can be a low-cost FPGA prototyping platforms, such as  the Altera Cyclone-IV Terasic DE10-Lite . The repository  includes project files and pin assignments for both these boards. The code is written in VHDL 
FPGAs consist of a matrix of programmable logic blocks surrounded by programmable output input blocks. The whole is connected by a programmable interconnection network.
#### FPGA ####
FPGAs are distinct from other programmable circuit families while offering the highest level of logical integration.
There are 4 main categories available commercially:
Symmetrical table.
In column.
Seas of doors.
Hierarchical PLDs.


### 2.1.Voltage levels ### 
It is very important to choose the right  I/O voltage levels of the devices match. Both FPGA boards support 3.3V levels, and are a good match for the Arduino 101. besides , the Arduino UNO uses the traditional 5 Volt TTL levels. Instead of using a level shifter we convert  the Arduino to 3.3V according to Adafruit’s instructions. 

### 2.2.Signals ### 
The SPI interface is a 4 wire interface. The bus consists of 3 signals plus *a slave select* signal for each device.

*SCLK*: clock signal sent from the master to all slaves.

*MOSI*: serial data from the master to the slaves (Master Out-Slave In).

*MISO*: serial data from a slave to the master (Master In-Slave Out).

*SS*:  slave select signal for each slave.

Once the Arduino runs at 3.3V, connecting the two devices becomes trivial.

### 2.2.1. Pin outs ### 

![z](img/electronics/fpga/image1.png)

### 2.2.2. The physical connections ### 

![z](img/electronics/fpga/image2.png)

      
## 3. BYTE – PROTOCOL ## 

With the two circuits  physically connected, we must have  a protocol to transfer data. We chose the Serial Peripheral Interface (SPI)  to connect one master to one or more slaves.

### 3.1 Master/slave ### 
The SPI bus is controlled by a master that orchestrates the bus access. The master generates the control signals and regulates the data flow. The illustration below shows a master with three slaves. The master uses the Slave Select (SS) signal to select the slave.
 
![z](img/electronics/fpga/image3.png)


### 3.2 Parameters ###
SPI is also a protocol that provide us much  degrees of freedom. It is significant  that the master and slave must be in harmony on the voltage levels and maximum clock frequency. The SPI  clock phase (CPHA) and clock polarity (CPOL) present  four more degrees of freedom as shown in the table below.
SPI parameters

![z](img/electronics/fpga/image4.png)

For this level ,  we work with  *mode 3*, where the clock is high when idle ;  data is follow  the falling edge of the clock and latched on the rising edge.
### 3.3. Slave select ###
To more understand , we should  comprise the impact of the *slave select* (*SS**) signal that is used to address the slave devices.
 
 ![z](img/electronics/fpga/image6.png)

Slaves can only drive their output (*MISO*) line when *SS** is active, also they should tri-stated the output. The protocol can be out of order  into the following steps:

1.	 The master starts the communication by activating SS*

*  The slave reply by starting to drive its MISO output.
+	Meantime the master drives its MOSI output.

2.	 The master makes SCLK low.

+ On this falling edge, the master and slave drive their most important bit position (b7) on respectively their MOSI and MISO outputs.

3.	 The master makes SCLK high.

+ On this rising edge, the master and slave clock the input from their respectively MISO and MOSI inputs into the least important bit position (b0).

4.	 return to step 2. Until the least significant bit position (b0) has been sent.

5.	 When all bits are transmitted, the master will deactivate SS*.

### 3.4. Operation ###
The protocol is easiest explained with shift registers as shown in the illustration below. The master generates the SPI Clock (*SCLK*) to initiate the information exchange. Data is shifted on one edge of this clock and is sampled on the opposite edge when the data is stable.

 ![z](img/electronics/fpga/image5.png)

In mode 3, at the falling edge of *SCLK*, in first step ,both devices drive their most significant bit (*b7*) on their outgoing data line. On the rising edge, both devices clock in this bit into the least significant bit position (*b0*). After eight *SCLK* cycles, the master and slave have exchanged completely their values and each device processes the data received (e.g. writing it to memory). when there is more data to be exchanged, the registers are loaded with new data and the process repeats itself. Once all data is transmitted, the master stops the *SCLK* clock.
so :
1. The master outputs the clock signal.
2. The master switches the SS/CS pin to a low voltage state, which activates the slave.
3. The master sends the data one bit at a time to the slave along the MOSI line. The slave reads the bits as they are received.
4. If a response is needed, the slave returns data one bit at a time to the master along the MISO line. The master reads the bits as they are received.



## 4. BYTES EXCHANGE WITH ARDUINO AS MASTER ##
The Arduino is based on a  support library for the serial peripheral interface. This make  the implementation more easy . For the slave we used an Altera  implementation . 

## 5. BYTE EXCHANGE WITH A FPGA AS SLAVE ##
Implementing the SPI Slave on an FPGA is like old school digital electronics. My key takeaway is to think hardware, not programming. Implementing the [SPI protocol](https://coertvonk.com/hw/logic/connecting-fpga-and-arduino-using-spi-13067/3) on a FPGA is fairly straightforward for as long as we use a directly clocked sequential circuit while preventing clock domain crossings.

### 5.1. Sequential circuit ### 
virtually, two signals going to a single gate will not arrive there at the same time because the wire delays. This causes the output to for a few moment have an incorrect value. The problem compounds as the signal travels through more gates and wires,so more delays.

In Building Math Hardware we created elementary math operations using combinatorial circuits. That was OK, because we didn’t care about such output *glitches* caused by the input signals propagating to the outputs. From a demonstrator’s point of view it even made it more interesting. but with SPI master is different, because it requires the outputs to be stable at certain times.
 
 ![z](img/electronics/fpga/image7.png)

The solution is to introduce a clock signal, and store the signals in a flip-flop, DFF ,(registers) at the rising edge of that clock signal. We then only need to ensure that the longest delay from one flip-flop to the next is less that the clock period. This greatly simplifies the design process, at the cost of introducing some delay.and like this we synchronize the two signal

### 5.2. Clock domain ###
Field programmable gate arrays thrive on synchronous designs, but they don’t do well with clock signals that are asynchronous with its system clock.
 
We also need to avoid transferring data from a [flip-flop](https://coertvonk.com/family/school/inquiries/computer-math-inquiry-4245) driven by one clock to a flip-flop driven by another clock. This is called a *clock domain crossing* and might manifest itself in *metastability*, data loss or incoherence .We prevent clock domain crossings, by synchronizing the input signals to the FPGA clock using a traditional two-stage shift register as illustrated above.

+ The first flip-flop creates a synchronous version of the inputs by clocking it with the system clock. The input signal could change within the flip-flop’s *setup and hold times* and may take longer than a system clock cycle to settle to a stable value (metastability). That’s why it is ran through a second flip-flop.

+ The second flip-flop, makes it is very unlikely that this metastability propagates to the output.

+ Adding a third flip-flop gives us access to the previous value. Using the current and previous values, we can generate rise and fall signals as sown below.

  ![z](img/electronics/fpga/image8.png)

### 5.3. Operation ###
The main data object is an 8-bit register called DATA.

On a falling SCLK edge, the most significant bit from data is clocked into a register from where it is transmitted over its MISO output.

On a rising SCLK edge, the MOSI input is shifted into the least significant bit of data.

Once all eight bits are received, the byte is available as rx. This received byte rx should be read when rx Valid is active during a rising edge of the sysClk.

## 6. MESSAGE EXCHANGE PROTOCOL ##
The time has come to implement a status and register interface on top of the raw byte exchange. We define a few commands to retrieve the device status and access its 32-bit registers.

### 6.1. Commands ###
The first byte is defined as the command byte. The interpretation of the remaining bytes (if any) depends on this command. After the command is completed, a new command can be sent. The following commands will be supported:

+	**Read status (0x00)**: Reads the status byte.

First the master sends 0x00, and ignores the value returned;

the master then sends one dummy byte, to get the 8-bit status value in return.

+ **Read register (0x80 to 0x8F)**: Reads the value stored in one of the sixteen registers. 

The least significant four bits of the command indicate the register to read from.
First the master sends this command, and ignores the value returned,then the master sends 4 dummy bytes to get the 32-bit register value. The first byte received is the most significant, the fourth is the least significant (network byte order).

+ **Write register (0xC0 to 0xCF)**: Writes a value to one of the sixteen registers. The least significant four bits indicate the register to write to.

  * First the master sends the command, and ignores the value returned;
  * Then the master sends 4 bytes with the value to write. The most significant byte is sent first, the least significant last.

### 6.2. Registers ###
The FPGA will implement two register types. The first 4 registers (0-3) are *read/write* and can be used to send information to the FPGA. The next 12 registers (4-15) are *read-only* to receive information from the FPGA. In the greater scheme, the *read/write* registers will be used to send math operands to the FPGA, and the read-only registers will be used to read the results from the FPGA.

### 6.3. Room for improvement ###
The protocol leaves some room for improvement. It can be made more efficient by implementing continuous commands. Here the master issues a *read* or *write register start* command, but keeps sending sets of 4-bytes until it has enough. Along similar lines one could implement commands to access attached memory.

## 7. MESSAGES EXCHANGE WITH ARDUINO AS MASTER ##

Again, we’ll use the support library for the serial peripheral interface. The code shown below was tested on a 3.3 Volt Arduino UNO R3 connected to FPGA implementation. 


