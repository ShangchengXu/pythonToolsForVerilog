class top_driver extends uvm_driver#(top_transaction);

   virtual top_if vif;

   `uvm_component_utils(top_driver)
   function new(string name = "top_driver", uvm_component parent = null);
      super.new(name, parent);
   endfunction

   virtual function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      if(!uvm_config_db#(virtual top_if)::get(this, "", "vif", vif))
         `uvm_fatal("top_driver", "virtual interface must be set for vif!!!")
   endfunction

   extern task main_phase(uvm_phase phase);
   extern task drive_one_pkt(top_transaction tr);
endclass

task top_driver::main_phase(uvm_phase phase);
   vif.data <= 8'b0;
   vif.valid <= 1'b0;
   while(!vif.rst_n)
      @(posedge vif.clk);
   while(1) begin
      seq_item_port.get_next_item(req);
      drive_one_pkt(req);
      seq_item_port.item_done();
   end
endtask

task top_driver::drive_one_pkt(top_transaction tr);
   byte unsigned     data_q[];
   int  data_size;
   
   data_size = tr.pack_bytes(data_q) / 8; 
   `uvm_info("top_driver", "begin to drive one pkt", UVM_LOW);
   repeat(3) @(posedge vif.clk);
   for ( int i = 0; i < data_size; i++ ) begin
      @(posedge vif.clk);
      vif.valid <= 1'b1;
      vif.data <= data_q[i]; 
   end

   @(posedge vif.clk);
   vif.valid <= 1'b0;
   `uvm_info("top_driver", "end drive one pkt", UVM_LOW);
endtask

