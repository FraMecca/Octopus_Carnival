main:
	rm deck/main.exe -f && \
	cd hosaka && dune build main.exe && \
	ln -s $(shell pwd)/hosaka/_build/default/main.exe ../deck/main.exe

tests:
	cd hosaka && corebuild tests.byte && ./tests.byte
