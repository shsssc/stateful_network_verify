Vagrant.configure("2") do |config|
  config.vm.define "stateful-verification-t"
  config.vm.hostname = "stateful-verification"
  config.vm.provider "docker" do |d|
    d.image = "klee/klee"
    d.cmd = ["sleep", "infinity"]
  end
end
