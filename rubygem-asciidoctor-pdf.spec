%global gem_name asciidoctor-pdf
%global mainver 1.5.0
%global prerelease .alpha.16
%global release 9

Name: rubygem-%{gem_name}
Version: %{mainver}
Release: %{?prerelease:0.}%{release}%{?prerelease}%{?dist}
Summary: Converts AsciiDoc documents to PDF using Prawn
License: MIT
URL: https://github.com/asciidoctor/asciidoctor-pdf
Source0: http://rubygems.org/gems/%{gem_name}-%{version}%{?prerelease}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel > 1.3.1
BuildRequires: ruby >= 1.9

BuildArch: noarch

%description
An extension for Asciidoctor that converts AsciiDoc documents to PDF using the
Prawn PDF library.

%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}%{?prerelease}
%gemspec_remove_dep -s ../%{gem_name}-%{version}%{?prerelease}.gemspec -g treetop "= 1.5.3"
%gemspec_remove_dep -s ../%{gem_name}-%{version}%{?prerelease}.gemspec -g prawn-icon "= 1.3.0"
%gemspec_remove_dep -s ../%{gem_name}-%{version}%{?prerelease}.gemspec -g prawn-svg ">= 0.21.0", "< 0.28.0"
%gemspec_add_dep -s ../%{gem_name}-%{version}%{?prerelease}.gemspec -g treetop "< 2.0.0"
%gemspec_add_dep -s ../%{gem_name}-%{version}%{?prerelease}.gemspec -g prawn-svg "~> 0.28.0"
%gemspec_add_dep -s ../%{gem_name}-%{version}%{?prerelease}.gemspec -g prawn-icon "~> 2.3.0"

%build
gem build ../%{gem_name}-%{version}%{?prerelease}.gemspec
%gem_install

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
%{_bindir}/%{gem_name}
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
%doc %{gem_instdir}/CHANGELOG.adoc
%doc %{gem_instdir}/docs
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile

%changelog
* Mon Apr 22 2019 Sergi Jimenez <tripledes@gmail.com> - 1.5.0-0.9.alpha.16
- Revert depending on prawn-svg 0.29.0.

* Sun Apr 14 2019 Sergi Jimenez <tripledes@gmail.com> - 1.5.0-0.8.alpha.16
- Fix BZ#1699514

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-0.7.alpha.16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 07 2018 Christopher Brown <chris.brown@redhat.com> - 1.5.0-0.6.alpha.16
- Update to 1.5.0.alpha.16

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-0.6.alpha.13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-0.5.alpha.13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-0.4.alpha.13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-0.3.alpha.13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 27 2016 Fabio Alessandro Locati <fale@redhat.com> - 1.5.0-0.2.alpha.13
- Update to 1.5.0.alpha.13

* Sun Aug 28 2016 Fabio Alessandro Locati <fale@redhat.com> - 1.5.0-0.2.alpha.12
- Update to 1.5.0.alpha.12

* Sun Aug 28 2016 Fabio Alessandro Locati <fale@redhat.com> - 1.5.0-0.2.alpha.11
- Provide asciidoctor-pdf for simpler searching

* Fri Jun 17 2016 Fabio Alessandro Locati <fale@redhat.com> - 1.5.0-0.1.alpha.11
- Initial package
