"""
 _____             _             _ _                 _                    
/  __ \           | |           | | |               (_)                   
| /  \/ ___  _ __ | |_ _ __ ___ | | |     ___   __ _ _  ___   _ __  _   _ 
| |    / _ \| '_ \| __| '__/ _ \| | |    / _ \ / _` | |/ __| | '_ \| | | |
| \__/\ (_) | | | | |_| | | (_) | | |___| (_) | (_| | | (__ _| |_) | |_| |
 \____/\___/|_| |_|\__|_|  \___/|_\_____/\___/ \__, |_|\___(_) .__/ \__, |
                                                __/ |        | |     __/ |
                                               |___/         |_|    |___/ 

@author Simon Gardier
"""

#STANDARD for values in control logic : | 2 bits | 1 bit  |1bit| 2 bits| 1 bit | 1 bit | 4 bits |
#                                       |  PCSEL | RA2SEL | WR | WDSEL |  BSEL |  WERF |  ALUFN |
ALUFN_POS = 0
WERF_POS = 4
BSEL_POS = 5
WDSEL_POS = 6
WR_POS = 8
RA2SEL_POS = 9
PCSEL_POS = 10

opcodes_alu = [
    #for two registers, WERF = 1, BSEL = 1
    0x20,#AND                           |       000000000      |   1   |  1    |  0001  |
    0x21,#SUB                           |       000000000      |   1   |  1    |  0010  |   
    0x22,#MUL                           |       000000000      |   1   |  1    |  0011  |
    0x23,#DIV

    0x28,#AND
    0x29,#OR
    0x2A,#XOR

    0x24,#CMPEQ
    0x25,#CMPLT
    0x26,#CMPLE

    0x2C,#SHL
    0x2D,#SHR
    0x2E,#SRA
]

opcodes_alu_constant = [
    #for a register and a constant, WERF = 1, BSEL = 0
    0x30,#ADDC
    0x31,#SUBC
    0x32,#MULC
    0x33,#DIVC

    0x38,#ANDC
    0x39,#ORC
    0x3A,#XORC

    0x34,#CMPEQC
    0x35,#CMPLT
    0x36,#CMPLEC

    0x3C,#SHLC
    0x3D,#SHRC
    0x3E,#SRAC
]

opcode_branching = [
    0x1B,#JMP
    0x1D,#BEQ
    0x1E#BNE
]

#create the memory
control_logic_memory = []
for i in range(0, 64):
    control_logic_memory.append(0x000)


#put data at alu opcodes adresses
alu_multiplexer_choice = 0b0001
for i in range(len(opcodes_alu)):                                                                                
    control_logic_memory[opcodes_alu[i]]            = (alu_multiplexer_choice << ALUFN_POS) + (0b1 << WERF_POS) + (0b1 << BSEL_POS) + (0b1 << WDSEL_POS) + (0b0 << WR_POS) + (0b0 << RA2SEL_POS) + (0b0 << PCSEL_POS)
    alu_multiplexer_choice += 1

#put data at alu constant opcodes adresses
alu_multiplexer_choice = 0b0001
for i in range(len(opcodes_alu)):
                                                
    control_logic_memory[opcodes_alu_constant[i]]   = (alu_multiplexer_choice << ALUFN_POS)  + (0b1 << WERF_POS) + (0b0 << BSEL_POS) + (0b1 << WDSEL_POS) + (0b0 << WR_POS) + (0b0 << RA2SEL_POS) + (0b0 << PCSEL_POS)
    alu_multiplexer_choice += 1

#put data at branching opcodes adresses
alu_multiplexer_choice = 0b0000 #dont care
pcsel_type = 0b1
for i in range(len(opcode_branching)):        
    control_logic_memory[opcode_branching[i]]       = (alu_multiplexer_choice << ALUFN_POS)  + (0b1 << WERF_POS) + (0b0 << BSEL_POS) + (0b0 << WDSEL_POS) + (0b0 << WR_POS) + (0b0 << RA2SEL_POS) + (pcsel_type << PCSEL_POS)
    pcsel_type += 1

#put data at data memory operations opcodes adresses
control_logic_memory[0x18]       = (0b0001 << ALUFN_POS)  + (0b1 << WERF_POS) + (0b0 << BSEL_POS) + (0b10 << WDSEL_POS) + (0b0 << WR_POS) + (0b0 << RA2SEL_POS) + (0b00 << PCSEL_POS)
control_logic_memory[0x19]       = (0b0001 << ALUFN_POS)  + (0b0 << WERF_POS) + (0b0 << BSEL_POS) + (0b00 << WDSEL_POS) + (0b1 << WR_POS) + (0b1 << RA2SEL_POS) + (0b00 << PCSEL_POS)


#write in file
f = open("controllLogic.txt", "w")
f.write("v2.0 raw\n")
for i in range(len(control_logic_memory)):
    f.write(hex(control_logic_memory[i])[2:]+" ")
    #Go to the line at each 16 values (to make the file more readable)
    if (i + 1) % 16 == 0:
        f.write("\n")
f.close()

