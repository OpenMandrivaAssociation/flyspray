%define name    flyspray
%define version 0.9.8
%define release %mkrel 1

Summary:	A simple Bug tracking system
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/WWW
Url:		http://flyspray.rocks.cc/
Source0:	http://flyspray.rocks.cc/files/%{name}-%{version}.tar.bz2
Requires:	apache-mod_php >= 2.0.54
Requires:	php-adodb >= 1:4.64-1mdk
BuildRequires:	apache-base >= 2.0.54-5mdk
BuildArch:	noarch

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
mkdir -p %{buildroot}%{_var}/www/%{name}
cp -R * %{buildroot}%{_var}/www/%{name}
mkdir -p %{buildroot}/%{_datadir}/%{name}/
mv  %{buildroot}%{_var}/www/%{name}/sql %{buildroot}/%{_datadir}/%{name}

mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
mv %{buildroot}%{_var}/www/%{name}/header.php %{buildroot}/%{_sysconfdir}/%{name}/
perl -pi -e 's#/var/www/flyspray#%{_var}/www/flyspray#' %{buildroot}/%{_sysconfdir}/%{name}/header.php


cat >  %{buildroot}%{_var}/www/%{name}/header.php <<EOF
<?
include('%{_sysconfdir}/%{name}/header.php');
?>
EOF


cat > %{buildroot}%{_var}/www/%{name}/not_configurated.html <<EOF
<html>
<body>
	Flyspray is not configured, please see %_defaultdocdir/%{name}-%{version}/README.POST
</body>
</html>
EOF

mkdir -p  %{buildroot}/%{_sysconfdir}/httpd/conf/webapps.d
cat > %{buildroot}/%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf << EOF
# This file add a redirection to the not_configurated.html 
# in order to warn people and do not use a service with
# bad default ( think super, super as a login password..)

AliasMatch /flyspray/* /var/www/flyspray/not_configurated.html

#Alias /%{name} %{_var}/www/%{name}
<Directory %{_var}/www/%{name}>
    Allow from all
</Directory>
EOF

cat > README.POST << EOF
The configuration file was moved to %{_sysconfdir}/%{name}/.

After the install of the rpm, you need to follow these step :

1) Set up your database, you need to create the table with the help
of the files in %{_datadir}/%{name}/sql subdirectory.
Do not forget to install the php module you need ( php-mysql or php-pgsql ),
and to reload apache after that.

2) Edit  %{_sysconfdir}/%{name}/header.php, to adapt it to your need.
The cookie have been already changed during the installation of the rpm.

3) Remove the first restriction in the file /etc/http/conf.d/flyspray.conf

4) Use the page http://localhost/flyspray/ to add a normal user
and remove the super user ( password and user are 'super', so this is
not good to keep them ).

5) Finish to configure flyspray as you want, and adjust the apache
configuration file to your need.
Do not forget to set base url trough the Admin menu.
EOF

%clean
rm -rf %buildroot

%post 
%_post_webapp
if [ "$1" = 1 ]; then
	cookie=`head /dev/urandom | md5sum | cut -b 1-16 `
	perl -pi -e "s#\\\$cookiesalt = .*#\\\$cookiesalt = '$cookie';#" %{_sysconfdir}/%{name}/header.php
fi

%postun 
%_postun_webapp

%files
%defattr(0644,root,root,0755)
%doc docs/* README.* sql/*sql
%{_var}/www/%{name}
%dir %attr(0755,apache,apache) %{_var}/www/%{name}/attachments/
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf

