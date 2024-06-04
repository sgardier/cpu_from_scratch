|;  ______ ___  _____ _____  ___   ________  ___
|;  |  ___/ _ \/  __ \_   _|/ _ \ /  ___|  \/  |
|;  | |_ / /_\ \ /  \/ | | / /_\ \\ `--.| .  . |
|;  |  _||  _  | |     | | |  _  | `--. \ |\/| |
|;  | |  | | | | \__/\ | |_| | | |/\__/ / |  | |
|;  \_|  \_| |_/\____/ \_(_)_| |_/\____/\_|  |_/
|;
|;  @author Simon Gardier

.include beta.uasm      |; include beta.uasm file for macro definition

|;------ Initialization code ------
CMOVE(3, r0)            |; value for which we want to compute the factorial
CMOVE(1, r1) 

|;------ Factorial code ------
BEQ(r0, fact_end, r31)  |; if r0 is 0, no need to compute factorial
fact:
  MUL(r1, r0, r1)       |; multiply r1 by r0
  SUBC(r0, 1, r0)       |; decrement r0
  BEQ(r0, fact_end, r31)|; if r0 is 0, stop algorithm
  BR(fact)              |; else loop
fact_end:
  ST(r1, 0)             |; store result in data memory

