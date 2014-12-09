ASFLAGS := -m32
CFLAGS  := -m32 -g -std=c99 -Wall -Werror -D_GNU_SOURCE
LDFLAGS := -m32
LDLIBS  := -lcrypto
PROGS   := zookld zookd zookfs 

all: $(PROGS)
.PHONY: all

zookld: zookld.o http.o
	cc $(LDFLAGS) zookld.o http.o $(LDLIBS) -o zookld
zookd: zookd.o http.o
	cc $(LDFLAGS) zookd.o http.o $(LDLIBS) -o zookd
zookfs: zookfs.o http.o
	cc $(LDFLAGS) zookfs.o http.o $(LDLIBS) -o zookfs
	
#	gcc zookld.o -o zookld
#	gcc zookd.o -o zookd
#	gcc zookfs.o -o zookfs
#	gcc http.o -o httpd

#zookld.o:
#	gcc $(CFLAGS) -c zookld.c

#zookd.o:
#	gcc $(CFLAGS)-c zookd.c

#zookfs.o:
#	gcc $(CFLAGS)-c zookfs.c

#http.o:
#	gcc $(CFLAGS)-c http.c
	
.PHONY: setup
setup:
	./chroot-setup.sh

.PHONY: fix-flask
fix-flask: fix-flask.sh
	./fix-flask.sh

.PHONY: clean
clean:
	rm -f *.o *.pyc *.bin $(PROGS)

