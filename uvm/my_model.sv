class my_model extends uvm_component;
   
   uvm_blocking_get_port #(uvm_sequence_item)  port;
   uvm_analysis_port #(uvm_sequence_item)  ap;

   extern function new(string name, uvm_component parent);
   extern function void build_phase(uvm_phase phase);
   extern virtual  task main_phase(uvm_phase phase);

   `uvm_component_utils(my_model)
endclass 

function my_model::new(string name, uvm_component parent);
   super.new(name, parent);
endfunction 

function void my_model::build_phase(uvm_phase phase);
   super.build_phase(phase);
   port = new("port", this);
   ap = new("ap", this);
endfunction

task my_model::main_phase(uvm_phase phase);
   uvm_sequence_item drive_req;
   my_transaction drive_tr;
   my_transaction scb_tr;
   super.main_phase(phase);
   while(1) begin
      port.get(drive_req);
      $cast(drive_tr,drive_tr);
      scb_tr = new("scb_tr");
      ap.write(scb_tr);
   end
endtask