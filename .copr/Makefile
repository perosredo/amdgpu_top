srpm:
	dnf install -y rpmdevtools
	rpmbuild -bs --define "_sourcedir ." --define "_specdir ." --define "_builddir ." --define "_srcrpmdir $(outdir)" --define "_rpmdir ." amdgpu_top.spec