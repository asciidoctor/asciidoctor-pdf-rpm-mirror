%global gem_name asciidoctor-pdf
%global mainver 1.5.0
%global prerelease .beta.6
%global release 12

%bcond_with network

Name: rubygem-%{gem_name}
Version: %{mainver}
Release: %{?prerelease:0.}%{release}%{?prerelease}%{?dist}
Summary: Converts AsciiDoc documents to PDF using Prawn
License: MIT
URL: https://github.com/asciidoctor/asciidoctor-pdf
Source0: http://rubygems.org/gems/%{gem_name}-%{version}%{?prerelease}.gem
# git clone https://github.com/asciidoctor/asciidoctor-pdf.git && cd asciidoctor-pdf
# git checkout v1.5.0.beta.6
# tar -czf rubygem-asciidoctor-pdf-1.5.0.beta.6.tgz spec/
Source1: %{name}-%{version}%{?prerelease}-specs.tgz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel > 1.3.1
BuildRequires: ruby >= 1.9
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(asciidoctor)
BuildRequires: rubygem(prawn)
BuildRequires: rubygem(prawn-svg)
BuildRequires: rubygem(prawn-table)
BuildRequires: rubygem(prawn-templates)
BuildRequires: rubygem(prawn-icon)
BuildRequires: rubygem(treetop)
BuildRequires: rubygem(concurrent-ruby)
BuildRequires: rubygem(safe_yaml)
BuildRequires: rubygem(chunky_png)
BuildRequires: rubygem(pdf-inspector)
BuildRequires: rubygem(rouge)
BuildRequires: rubygem(coderay)
BuildRequires: rubygem(thread_safe)

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
%setup -q -n %{gem_name}-%{version}%{?prerelease} -b 1

# Regenerate the parser.
tt lib/asciidoctor/pdf/formatted_text/parser.treetop

%gemspec_remove_dep -g treetop '~> 1.5.0'
%gemspec_add_dep -g treetop '~> 1.5'
%gemspec_remove_dep -g concurrent-ruby '~> 1.1.0'
%gemspec_add_dep -g concurrent-ruby '~> 1.0'

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

%check
pushd .%{gem_instdir}
cp -a %{_builddir}/{spec,examples} .

%if ! %{with network}
# These tests require network connectivity.
sed -i "/it 'should read remote image if allow-uri-read is set' do/a\\
      skip" spec/image_spec.rb
sed -i "/it 'should use image format specified by format attribute' do/a\\
      skip" spec/image_spec.rb
sed -i "/video_id = '77477140'/i\\
      skip" spec/video_spec.rb
%endif

rspec spec \
  | tee /dev/stderr \
  | grep '624 examples, 14 failures, 3 pending'
popd

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
%doc %{gem_instdir}/.yardopts
%{gem_instdir}/%{gem_name}.gemspec

%changelog
* Wed Oct 30 2019 Christopher Brown <chris.brown@redhat.com> - 1.5.0-0.12.beta.6
- Relax Concurrent dependency.

* Tue Oct 29 2019 Vít Ondruch <vondruch@redhat.com> - 1.5.0-0.12.beta.6
- Disable network depending tests.
- Relax Treetop dependency.

* Sat Oct 19 2019 Christopher Brown <chris.brown@redhat.com> - 1.5.0-0.11.beta.6
- Update to 1.5.0.beta.6
- Enable test suite

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-0.10.alpha.18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 26 2019 Christopher Brown <chris.brown@redhat.com> - 1.5.0-0.9.alpha.18
- Update to 1.5.0.alpha.18

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
