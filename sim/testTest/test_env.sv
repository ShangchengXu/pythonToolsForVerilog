class test_env extends uvm_env;

   test_agent   i_agt;
   test_agent   o_agt;
   test_model   mdl;
   test_scoreboard scb;
   
   uvm_tlm_analysis_fifo #(test_transaction) agt_scb_fifo;
   uvm_tlm_analysis_fifo #(test_transaction) agt_mdl_fifo;
   uvm_tlm_analysis_fifo #(test_transaction) mdl_scb_fifo;
   
   function new(string name = "test_env", uvm_component parent);
      super.new(name, parent);
   endfunction

   virtual function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      i_agt = test_agent::type_id::create("i_agt", this);
      o_agt = test_agent::type_id::create("o_agt", this);
      i_agt.is_active = UVM_ACTIVE;
      o_agt.is_active = UVM_PASSIVE;
      mdl = test_model::type_id::create("mdl", this);
      scb = test_scoreboard::type_id::create("scb", this);
      agt_scb_fifo = new("agt_scb_fifo", this);
      agt_mdl_fifo = new("agt_mdl_fifo", this);
      mdl_scb_fifo = new("mdl_scb_fifo", this);

   endfunction

   extern virtual function void connect_phase(uvm_phase phase);
   
   `uvm_component_utils(test_env)
endclass

function void test_env::connect_phase(uvm_phase phase);
   super.connect_phase(phase);
   i_agt.ap.connect(agt_mdl_fifo.analysis_export);
   mdl.port.connect(agt_mdl_fifo.blocking_get_export);
   mdl.ap.connect(mdl_scb_fifo.analysis_export);
   scb.exp_port.connect(mdl_scb_fifo.blocking_get_export);
   o_agt.ap.connect(agt_scb_fifo.analysis_export);
   scb.act_port.connect(agt_scb_fifo.blocking_get_export); 
endfunction
