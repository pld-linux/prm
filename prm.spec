# NOTE:
#  - file /usr/bin/prm from install of prm-0.2.13-1.noarch conflicts with file from package synce-core-0.17-2.x86_64
Summary:	Package Repository Manager
Name:		prm
Version:	0.2.13
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{name}-%{version}.gem
# Source0-md5:	7d01b989cb87510addc64686d5deb5f9
Patch0:		optional-s3.patch
Patch1:		templates.patch
URL:		https://github.com/dnbert/prm
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	sed >= 4.0
Requires:	ruby-arr-pm
Requires:	ruby-clamp
Requires:	ruby-peach
Suggests:	ruby-aws-s3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PRM (Package Repository Manager) is an Operating System independent
Package Repository tool. It allows you to quickly build Debian and Yum
Package Repositories. PRM can sync local repositories to S3 compatible
object storage systems.

%prep
%setup -q
%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*
%patch0 -p1
%patch1 -p1

# remove +x to avoid generating bogus deps
find lib -type f | xargs chmod a-x

%build
# write .gemspec
%__gem_helper spec
# make aws/s3 optional
%{__sed} -i -e '/aws-s3/d' *.gemspec

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir},%{_bindir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a templates $RPM_BUILD_ROOT%{ruby_vendorlibdir}/%{name}
cp -p %{name}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/prm
%{ruby_vendorlibdir}/%{name}.rb
%{ruby_vendorlibdir}/%{name}
%{ruby_specdir}/%{name}-%{version}.gemspec
