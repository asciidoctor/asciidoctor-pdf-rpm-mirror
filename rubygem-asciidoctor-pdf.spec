%global gem_name asciidoctor-pdf
%global mainver 1.5.0
%global prever .alpha.11
%global release 2
%{?prever:
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{mainver}%{?prever}
%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{mainver}%{?prever}
%global gem_cache %{gem_dir}/cache/%{gem_name}-%{mainver}%{?prever}.gem
%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{mainver}%{?prever}.gemspec
}

Name: rubygem-%{gem_name}
Version: %{mainver}
Release: %{?prever:0.}%{release}%{?prever}%{?dist}
Summary: Converts AsciiDoc documents to PDF using Prawn
Group: Development/Languages
License: MIT
URL: https://github.com/asciidoctor/asciidoctor-pdf
Source0: http://rubygems.org/gems/%{gem_name}-%{version}%{?prever}.gem
# Workaround to very strict dependencies
Patch0: asciidoctor-pdf-fix-dependencies.patch
Provides: asciidoctor-pdf = %{version}
BuildRequires: ruby(release)
BuildRequires: rubygems-devel > 1.3.1
BuildRequires: ruby >= 1.9
Requires: ruby(release)
Requires: ruby(rubygems)

BuildArch: noarch

%description
An extension for Asciidoctor that converts AsciiDoc documents to PDF using the
Prawn PDF library.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}%{?prever}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%patch0

%build
gem build %{gem_name}.gemspec
%gem_install -n%{gem_name}-%{version}%{?prever}.gem

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/
mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%files
%dir %{gem_instdir}
%{_bindir}/asciidoctor-pdf
%license %{gem_instdir}/LICENSE.adoc
%doc %{gem_instdir}/README.adoc
%{gem_instdir}/bin
%{gem_instdir}/data
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/NOTICE.adoc
%doc %{gem_instdir}/docs
%{gem_instdir}/Rakefile

%changelog
* Sun Aug 28 2016 Fabio Alessandro Locati <fale@redhat.com> - 1.5.0-0.2.alpha.11
- Provide asciidoctor-pdf for simpler searching

* Fri Jun 17 2016 Fabio Alessandro Locati <fale@redhat.com> - 1.5.0-0.1.alpha.11
- Initial package
