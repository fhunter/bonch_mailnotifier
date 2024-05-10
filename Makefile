all: deb

tree: mailnotify.py mailnotify.desktop control
	mkdir -p target
	mkdir -p target/DEBIAN
	mkdir -p target/usr/share/applications/
	mkdir -p target/usr/bin
	cp control target/DEBIAN
	cp mailnotify.py target/usr/bin/
	cp mailnotify.desktop target/usr/share/applications/

deb: tree
	fakeroot dpkg -b ./target/ ./
