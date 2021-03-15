NAME=monitoring-aws
VERSION?=SNAPSHOT
TGZ=${NAME}-${VERSION}.tgz

all: clean archive 
	
archive: ${TGZ}

${TGZ}:
	@echo "Creating ${TGZ} ..."
	@tar zcf ${TGZ} bin
	@sha512sum ${TGZ} | tee ${NAME}-${VERSION}.sha

clean:
	@rm -f ${TGZ}
