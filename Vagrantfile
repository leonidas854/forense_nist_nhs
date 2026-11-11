# frozen_string_literal: true
require 'json'

unless ENV.fetch('VAGRANT_EXPERIMENTAL', '').split(',').include?('none_communicator')
  raise 'Usa ./lab en lugar de vagrant; activa el comunicador sin red antes de cargar plugins.'
end

settings_path = File.join(__dir__, 'local', 'settings.json')
settings = File.exist?(settings_path) ? JSON.parse(File.read(settings_path)) : {}
windows_iso = ENV.fetch('WIN10_ISO', settings.fetch('windows_iso', ''))
tools_iso = File.join(__dir__, 'local', 'herramientas.iso')

Vagrant.configure('2') do |config|
  # Box local de hardware vacío: Windows se instala con la ISO propia.
  config.vm.box = 'nhs/windows10-installer'
  config.vm.box_check_update = false
  config.vm.communicator = 'none'
  config.vm.synced_folder '.', '/vagrant', disabled: true
  config.vm.network 'forwarded_port', guest: 22, host: 2222, id: 'ssh', disabled: true

  config.vm.provider 'virtualbox' do |vb|
    vb.name = 'forense-nhs-win10'
    vb.memory = 4096
    vb.cpus = 2
    vb.gui = ENV.fetch('LAB_GUI', 'true') == 'true'
    vb.check_guest_additions = false
    (1..8).each { |i| vb.customize ['modifyvm', :id, "--nic#{i}", 'none'] }
    vb.customize ['modifyvm', :id, '--clipboard-mode', 'disabled',
                  '--drag-and-drop', 'disabled', '--vrde', 'off',
                  '--usb-ohci', 'off', '--usb-ehci', 'off', '--usb-xhci', 'off',
                  '--audio-enabled', 'off', '--boot1', 'disk', '--boot2', 'dvd',
                  '--boot3', 'none', '--boot4', 'none']
    unless windows_iso.empty?
      raise "ISO inexistente: #{windows_iso}" unless File.file?(windows_iso)
      vb.customize ['storageattach', :id, '--storagectl', 'SATA', '--port', '1',
                    '--device', '0', '--type', 'dvddrive', '--medium', windows_iso]
    end
    if File.file?(tools_iso)
      vb.customize ['storageattach', :id, '--storagectl', 'SATA', '--port', '2',
                    '--device', '0', '--type', 'dvddrive', '--medium', tools_iso]
    end
  end
end
