%define name    flyspray
%define version 0.9.9.5.1
%define release %mkrel 1

Summary:    A simple Bug tracking system
Name:       %{name}
Version:    %{version}
Release:    %{release}
License:    GPLv2
Group:      Networking/WWW
Url:        http://flyspray.org
Source0:    http://flyspray.org/%{name}-%{version}.tar.bz2
Source1:	README.urpmi
Requires(pre):  rpm-helper   
Requires:   apache-mod_php >= 2.0.54
Requires:   php-adodb >= 1:4.64-1mdk
BuildRequires:  apache-base >= 2.0.54-5mdk
BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root

%description
%{name} is a simple bug tracking system, written in php, aimed
at people who do not want to deploy Bugzilla.
It offer most of the features needed without a increased complexity.
The configuration is done trough a web interface, and you can fully
control who can do what on the various task.

%prep
%setup -q

# strip away annoying ^M
find . -type f | perl -ne 'chomp; print "$_\n" if -T $_' | xargs perl -pi -e 'tr/\r//d'

%build


%install
rm -rf %buildroot
%__install -d -m 755 %{buildroot}%_defaultdocdir/%{name}
%__install -m 644 %{SOURCE1} %{buildroot}%_defaultdocdir/%{name}

%__install -d -m 755 %{buildroot}%{_var}/www/%{name}
cp -aRf * %{buildroot}%{_var}/www/%{name}

# remove .htaccess files
find %{buildroot}%{_var}/www/%{name} -name .htaccess -exec rm -f {} \;

# Create empty config file
%__install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
cat > %{buildroot}%{_sysconfdir}/%{name}/flyspray.conf.php <<EOF
# Configuration file for flyspray will be overide during configuration
EOF

ln -s %{_sysconfdir}/%{name}/flyspray.conf.php %{buildroot}%{_var}/www/%{name}/

%__install -d -m 755  %{buildroot}/%{_webappconfdir}
cat > %{buildroot}/%{_webappconfdir}/%{name}.conf << EOF

Alias /%{name} %{_var}/www/%{name}
<Directory %{_var}/www/%{name}>
    Allow from all
</Directory>

<Directory %{_var}/www/%{name}/adodb>
    Deny from all
</Directory>

<Directory %{_var}/www/%{name}/conf>
    Deny from all
</Directory>

<Directory %{_var}/www/%{name}/includes>
    Deny from all
</Directory>

<Directory %{_var}/www/%{name}/templates>
    Deny from all
</Directory>

<Files %{_var}/www/%{name}/plugins/*.php>
    Deny from all
</Files>

<Files %{_var}/www/%{name}/plugins/fetch.php>
    Allow from all
</Files>

EOF

%clean
rm -rf %buildroot

%post 
%_post_webapp

%postun 
%_postun_webapp

%files
%defattr(0644,root,root,0755)
%doc docs/* 
%{_var}/www/%{name}
%dir %attr(0755,apache,apache) %{_var}/www/%{name}/attachments/
%dir %attr(0755,apache,apache) %{_var}/www/%{name}/cache/
%config(noreplace) %attr(0755,apache,apache) %{_sysconfdir}/%{name}/flyspray.conf.php
%config(noreplace) %{_webappconfdir}/%{name}.conf

