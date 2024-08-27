ARG VARIANT
FROM checkmk/check-mk-raw:${VARIANT}

RUN /docker-entrypoint.sh /bin/true

USER cmk
ENV PATH=/omd/sites/cmk/bin:/omd/sites/cmk/local/lib/python3/bin/:$PATH
ENTRYPOINT ["/bin/bash"]
