`include "uvm_macros.svh"
module testTB;
test_interface_port ifo ();
test_interface_inner ifi ();
logic clk;
logic rst_n;
logic rst_p;
logic lklkl;
test test_inst (
        .a  (ifo.a) ,//input   [3:0]
        .b  (ifo.b) ,//input   [3:0]
        .c  (ifo.c) ,//output  [4:0]
        .l  (ifo.l));//output  
always #5 clk = ~clk;

initial begin
clk = 0;
rst_n = 0;
rst_p = 1;
#8 rst_n = 1;
#6 rst_p = 0;
lklkl = 0;

end

always@ * begin
ifo.clk <= clk;
ifo.rst_n <= rst_n;

end

initial begin
   run_test();
end

initial begin
   uvm_config_db#(virtual test_interface_port)::set(null, "uvm_test_top.env.i_agt.drv", "vif", ifo);
   uvm_config_db#(virtual test_interface_port)::set(null, "uvm_test_top.env.i_agt.mon", "vif", ifo);
   uvm_config_db#(virtual test_interface_port)::set(null, "uvm_test_top.env.o_agt.mon", "vif", ifo);
   uvm_config_db#(virtual test_interface_inner)::set(null, "uvm_test_top.env.i_agt.drv", "vif_i", ifi);
   uvm_config_db#(virtual test_interface_inner)::set(null, "uvm_test_top.env.i_agt.mon", "vif_i", ifi);
   uvm_config_db#(virtual test_interface_inner)::set(null, "uvm_test_top.env.o_agt.mon", "vif_i", ifi);
end






endmodule
