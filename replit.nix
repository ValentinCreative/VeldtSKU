{ pkgs }: {
  deps = [
    pkgs.gdb
    pkgs.glibcLocales
    pkgs.glibc
    pkgs.replitPackages.prybar-python3
  ];
}