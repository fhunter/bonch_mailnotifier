all: deb

tree: src/mailnotify.py mailnotify.desktop control
	mkdir -p target
	mkdir -p target/DEBIAN
	mkdir -p target/usr/share/applications/
	mkdir -p target/usr/bin
	cp control target/DEBIAN
	cp src/mailnotify.py target/usr/bin/
	cp mailnotify.desktop target/usr/share/applications/

deb: tree
	fakeroot dpkg -b ./target/ ./
