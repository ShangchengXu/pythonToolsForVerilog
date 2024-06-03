class my_case0_sequence extends uvm_sequence #(uvm_sequence_item);
   my_transaction m_trans;

   function  new(string name= "my_case0_sequence");
      super.new(name);
   endfunction 
   
   virtual task body();
      repeat (10) begin
         `uvm_do(m_trans)
      end
   endtask

   `uvm_object_utils(my_case0_sequence)
endclass