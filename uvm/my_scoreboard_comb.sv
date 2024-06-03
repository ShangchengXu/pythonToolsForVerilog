class my_scoreboard extends uvm_scoreboard;
   my_transaction  expect_queue[$];
   uvm_blocking_get_port #(uvm_sequence_item)  exp_port;
   uvm_blocking_get_port #(uvm_sequence_item)  act_port;
   `uvm_component_utils(my_scoreboard)

   extern function new(string name, uvm_component parent = null);
   extern virtual function void build_phase(uvm_phase phase);
   extern virtual task main_phase(uvm_phase phase);
endclass 

function my_scoreboard::new(string name, uvm_component parent = null);
   super.new(name, parent);
endfunction 

function void my_scoreboard::build_phase(uvm_phase phase);
   super.build_phase(phase);
   exp_port = new("exp_port", this);
   act_port = new("act_port", this);
endfunction 

task my_scoreboard::main_phase(uvm_phase phase);
   uvm_sequence_item  get_expect,  get_actual;
   my_transaction  expect_tr,  actual_tr;
   bit result;
 
   super.main_phase(phase);
   fork 
      // while (1) begin
      //    exp_port.get(get_expect);
      //    expect_queue.push_back(get_expect);
      // end
      while (1) begin
         act_port.get(get_actual);
         exp_port.get(get_expect);
         $cast(expect_tr,get_expect);
         $cast(actual_tr,get_actual);
         // if(expect_queue.size() > 0) begin
            // tmp_tran = expect_queue.pop_front();
         result = actual_tr.compare(expect_tr);
         if(result) begin 
            `uvm_info("my_scoreboard", "Compare SUCCESSFULLY", UVM_LOW);
         end
         else begin
            `uvm_error("my_scoreboard", "Compare FAILED");
         end
         // end
         // else begin
            // `uvm_error("my_scoreboard", "Received from DUT, while Expect Queue is empty");
         // end 
      end
   join
endtask