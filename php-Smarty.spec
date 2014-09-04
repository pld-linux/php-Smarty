#
# Conditional build:
%bcond_with	bc		# build BC wrapper as default Smarty class

%define		main_version 3.1.19
%define		doc_version	3.1.14
%define		rel	1
%define		php_min_version 5.2.0
Summary:	Template engine for PHP
Summary(pl.UTF-8):	System szablonów dla PHP
Name:		php-Smarty
Version:	%{main_version}
Release:	%{rel}%{?with_bc:BC}
License:	LGPL v3
Group:		Development/Languages/PHP
Source0:	http://www.smarty.net/files/Smarty-%{version}.tar.gz
# Source0-md5:	8db6f31fcf80aa0e0cbb064112fbb1bd
# Source1Download: http://www.smarty.net/documentation
Source1:	http://www.smarty.net/files/docs/manual-en.%{doc_version}.zip
# Source1-md5:	f54b1dd458776e4b1ccfdbfbfda1f484
Patch0:		bc.patch
URL:		http://www.smarty.net/
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.553
BuildRequires:	unzip
Requires:	php(core) >= %{php_min_version}
Requires:	php(date)
Requires:	php(mbstring)
Requires:	php(pcre)
Requires:	php(tokenizer)
%if %{with bc}
Provides:	Smarty = %{version}
Obsoletes:	Smarty < 3.0
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		appdir		%{php_data_dir}/Smarty3

%description
Smarty is a template engine for PHP. Smarty provides your basic
variable substitution and dynamic block functionality, and also takes
a step further to be a "smart" template engine, adding features such
as configuration files, template functions, variable modifiers, and
making all of this functionality as easy as possible to use for both
programmers and template designers.

%{?with_bc:This package is modified to have SmartyBC class as Smarty
class name}

%description -l pl.UTF-8
Smarty jest systemem szablonów dla PHP. Pozwala na podstawowe
podstawianie wartości zmiennych oraz dynamiczne operacje na blokach;
idzie o krok dalej, aby być "mądrym" silnikiem szablonów, dodając
takie możliwości jak pliki konfiguracyjne, funkcje, zmienne
modyfikatory oraz czyniąc całą funkcjonalność jak najłatwiejszą w
użyciu jednocześnie dla programistów i projektantów szablonów.

%package doc
Summary:	Template engine for PHP - documentation
Summary(pl.UTF-8):	System szablonów dla PHP - dokumentacja
Version:	%{doc_version}
Group:		Development/Languages/PHP

%description doc
Documentation for Smarty template engine.

%description doc -l pl.UTF-8
Dokumentacja do systemu szablonów Smarty.

%prep
%setup -q -n Smarty-%{main_version} -a1
%undos -f php

%if %{with bc}
mv libs/Smarty.class.php libs/Smarty3.class.php
mv libs/SmartyBC.class.php libs/Smarty.class.php
%patch0 -p1
%endif

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{appdir}
cp -a libs/* $RPM_BUILD_ROOT%{appdir}

%if %{with bc}
ln -s Smarty3/Smarty.class.php $RPM_BUILD_ROOT%{php_data_dir}
ln -s Smarty3 $RPM_BUILD_ROOT%{php_data_dir}/Smarty
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with bc}
# compat symlink, but need to mv dir first due rpm dir-symlink issue
%pretrans
test -L %{php_data_dir}/Smarty && exit 0
if [ -d %{php_data_dir}/Smarty/plugins ]; then
	mv %{php_data_dir}/Smarty/plugins/* %{appdir}/plugins
	rmdir %{php_data_dir}/Smarty/plugins 2>/dev/null
fi
rmdir %{php_data_dir}/Smarty 2>/dev/null || mv -v %{php_data_dir}/Smarty{,.rpmsave}
ln -s Smarty3 %{php_data_dir}/Smarty
%endif

%files
%defattr(644,root,root,755)
%doc README SMARTY_3.1_NOTES.txt
%dir %{appdir}
%dir %{appdir}/plugins
%dir %{appdir}/sysplugins
%{appdir}/Smarty.class.php
%{appdir}/SmartyBC.class.php
%{appdir}/debug.tpl
%{appdir}/plugins/*.php
%{appdir}/sysplugins/*.php

%if %{with bc}
%{appdir}/Smarty3.class.php
%{php_data_dir}/Smarty.class.php
%{php_data_dir}/Smarty
%endif

%files doc
%defattr(644,root,root,755)
%doc demo manual-en
