srpm:
	dnf install -y rpmdevtools
	tar --exclude=.git --exclude=target -czf amdgpu_top-0.10.5.tar.gz .
	rpmbuild -bs --define "_sourcedir ." --define "_specdir ." --define "_builddir ." --define "_srcrpmdir $(outdir)" --define "_rpmdir ." amdgpu_top.spec