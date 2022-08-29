#define __debug_package %{nil}
#define _debug_package %{nil}
%define debug_package %{nil}
#define pre rc2

Name:		ipp-usb
Version:	0.9.22
Release:	1
Summary:	IPP-over-USB implementation
License:	MIT
Group:		Hardware
Url:		https://github.com/OpenPrinting/ipp-usb
Source0:	https://github.com/OpenPrinting/ipp-usb/archive/refs/tags/%{version}.tar.gz
BuildRequires:	golang make

%description
IPP-over-USB allows using the IPP protocol, normally designed for network
printers, to be used with USB printers as well.

The idea behind this standard is simple: It allows to send HTTP requests
to the device via a USB connection, so enabling IPP, eSCL (AirScan) and
web console on devices without Ethernet or WiFi connections.

Unfortunately, the naive implementation, which simply relays a TCP connection
to USB, does not work. It happens because closing the TCP connection on the
client side has a useful side effect of discarding all data sent to this
connection from the server side, but it does not happen with USB
connections.

In the case of USB, all data not received by the client will remain in the
USB buffers, and the next time the client connects to the device, it will
receive unexpected data, left from the previous abnormally completed
request.

Actually, it is an obvious flaw in the IPP-over-USB standard, but we have
to live with it.

So the implementation, once the HTTP request is sent, must read the entire
HTTP response, which means that the implementation must understand the HTTP
protocol, and effectively implement a HTTP reverse proxy, backed by the
IPP-over-USB connection to the device.

And this is what the ipp-usb program actually does.

%prep
%autosetup -p1

%build
%make_build

%install
%make_install
mkdir -p %{buildroot}%{_bindir}
mv %{buildroot}/sbin/* %{buildroot}%{_bindir}
mv %{buildroot}/lib %{buildroot}%{_prefix}

%files
%{_bindir}/*
%{_sysconfdir}/ipp-usb
%{_prefix}/lib/systemd/system/ipp-usb.service
%{_prefix}/lib/udev/rules.d/71-ipp-usb.rules
%{_datadir}/ipp-usb
%{_mandir}/man8/*
