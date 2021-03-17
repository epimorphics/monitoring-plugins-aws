NAME=monitoring-aws
VERSION?=SNAPSHOT
DIR=release
ROOT=${DIR}/${NAME}-${VERSION}
TGZ=${ROOT}.tgz
SHA=${ROOT}.sha

all: clean product
	
arch: product

${DIR}:
	@mkdir $@

product: ${DIR}
	@echo "Creating ${TGZ} ..."
	@tar zcf ${TGZ} bin
	@sha512sum ${TGZ} | tee ${SHA}

clean:
	@rm -rf ${DIR}

env:
	@env > env.txt
	@cat env.txt
