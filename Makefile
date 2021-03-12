NAME=monitoring-aws
VERSION?=SNAPSHOT
TGZ=${NAME}-${VERSION}.tgz

all: archive 
	
archive: ${TGZ}

${TGZ}:
	@echo "Creating ${TGZ} ..."
	@tar zcf ${TGZ} bin && echo Done.

clean:
	@rm -f ${TGZ}
