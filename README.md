localtable {destname: cost} starts with a statement self: 0
route_table {destname: (nexthop, cost)}
outports {destname: port}
inports [ports]
inport_names {port: name}
Table global
others local probably

TODO:
-Make the sent packets compatible with the RIP specification. This will require adding an encode function and a decode function so we can continue using dictionaries in the real code. Shouldn't be too complex
-Triggered updates only happen when a router cost = 16. This fixes an issue with timeout at the same time.
-Change last metric from the timeout function to use the initial routing table values
-Add something to not send to routers with a cost of 16, actually assume they're dead
-Error checking - test received packets and config files when starting
-Test on large scale networks
-BS some 'tests' for the report (only 15% of the mark tho so no biggie)
-Ensure we can describe the program effectively during marking
-Write the report

13/04/2023
--Making it so it complies with RIP specs
--Still don't know how the code is working


