from file_analyse import File_analyse
if __name__=="__main__":
	fp = open("./code/uart_byte_tx.v","r")
	string_test = fp.read()
	fp.close()
	fa = File_analyse(string_test)
	# fa.find_pair(string_test,"{","}")
	fa.text_used(string_test)

	fp = open("./out.v","w+")
	fp.write(fa.find_varDefine(string_test)[1])
	fp.close()