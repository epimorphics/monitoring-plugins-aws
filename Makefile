NAME?=monitoring-aws
VERSION?=SNAPSHOT
ROOT=${NAME}_${VERSION}
TGZ=${ROOT}.tar.gz
SHA=${ROOT}_sha512-checksums.txt
BONSAI=bonsai.yml

all: clean assets

assets: sha bonsai

bonsai: ${BONSAI}

${BONSAI}:
	@echo '---' > $@
	@echo 'description: "'${NAME}'"' >> $@
	@echo 'builds:' >> $@
	@echo '- platform: "linux"' >> $@
	@echo '  arch: "amd64"' >> $@
	@echo '  asset_filename: "'${TGZ}'"' >> $@
	@echo '  sha_filename: "'${SHA}'"' >> $@

sha: ${SHA}
	
${TGZ}:
	@echo "Creating ${TGZ} ..."
	@tar zcf ${TGZ} bin

${SHA}: ${TGZ}
	@sha512sum ${TGZ} | tee ${SHA}

clean:
	@rm -f ${TGZ} ${SHA} ${BONSAI}
