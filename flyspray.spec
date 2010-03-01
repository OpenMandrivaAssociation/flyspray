%define name    flyspray
%define version 0.9.9.6
%define release %mkrel 4

%define _requires_exceptions pear(Zend.*)

Summary:    A simple Bug tracking system
Name:       %{name}
Version:    %{version}
Release:    %{release}
License:    GPLv2
Group:      Networking/WWW
Url:        http://flyspray.org
Source0:    http://flyspray.org/%{name}-%{version}.tar.bz2
Requires:   apache-mod_php
Requires:   php-adodb
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}

%description
%{name} is a simple bug tracking system, written in php, aimed
at people who do not want to deploy Bugzilla.
It offer most of the features needed without a increased complexity.
The configuration is done trough a web interface, and you can fully
control who can do what on the various task.

%prep
%setup -q -c %{name}-%{release}

%build

%install
rm -rf %buildroot

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

cat > README.urpmi <<EOF
Once this package is installed, there are a few configuration items which need
to be performed before the blog is usable.  First, you need to install
Mysql or PostgreSQL database and corresponding php modules:

# urpmi mysql php-mysql

or 

# urpmi postgresql php-pgsql

Then, you need to establish a username and password to connect to your
MySQL database as, and make both MySQL/Postgres and Flyspray aware of this.
Let's start by creating the database and the username / password
inside MySQL first:

  # mysql
  mysql> create database flyspray;
  Query OK, 1 row affected (0.00 sec)

  mysql> grant all privileges on flyspray.* to flyspray identified by 'flyspray';
  Query OK, 0 rows affected (0.00 sec)

  mysql> flush privileges;
  Query OK, 0 rows affected (0.00 sec)

  mysql> exit
  Bye
  #

Under certain curcumstances, you may need to run variations of the "grant"
command:
mysql> grant all privileges on flyspray.* to flyspray@localhost identified by 'flyspray';
   OR
mysql> grant all privileges on flyspray.* to flyspray@'%' identified by 'flyspray';

This has created an empty database called 'flyspray', created a user named
'flyspray' with a password of 'flyspray', and given the 'flyspray' user total
permission over the 'flyspray' database.  Obviously, you'll want to select a
different password, and you may want to choose different database and user
names depending on your installation.  The specific values you choose are
not constrained, they simply need to be consistent between the database and the
config file.

Once that's done and the database server and web server have been started, 
 in your favourite web browser, enter following URL :
http://hostname/flyspray/  and 
follow the instructions given to you on the pages you see to set up the 
database tables and begin publishing your blog.
EOF

%clean
rm -rf %buildroot

%post 
%if %mdkversion < 201010
%_post_webapp
%endif

%postun 
%if %mdkversion < 201010
%_postun_webapp
%endif

%files
%defattr(-,root,root)
%doc docs/* 
%{_var}/www/%{name}
%dir %attr(0755,apache,apache) %{_var}/www/%{name}/attachments/
%dir %attr(0755,apache,apache) %{_var}/www/%{name}/cache/
%config(noreplace) %attr(0755,apache,apache) %{_sysconfdir}/%{name}/flyspray.conf.php
%config(noreplace) %{_webappconfdir}/%{name}.conf
