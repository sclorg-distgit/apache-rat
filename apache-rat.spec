%global pkg_name apache-rat
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

%global snapdate 20100827
#svn 990212.

Name:           %{?scl_prefix}%{pkg_name}
Version:        0.8
Release:        13.18%{?dist}
Summary:        Apache Release Audit Tool (RAT)

License:        ASL 2.0
URL:            http://creadur.apache.org/rat/
#svn had a number of needed bugfixes
#svn export -r 990212 http://svn.apache.org/repos/asf/incubator/rat/main/trunk apache-rat-0.8-20100707
#Source0:        %{pkg_name}-%{version}-%{snapdate}.tar.bz2
Source0:        http://www.apache.org/dist/incubator/rat/sources/apache-rat-incubating-%{version}-src.tar.bz2
Patch0:         apache-rat-0.8-doxia-1.1.patch
Patch1:         apache-rat-compat.patch
Patch2:         apache-rat-0.8-test.patch
BuildArch:      noarch

BuildRequires:  %{?scl_prefix_java_common}javapackages-tools
BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  maven30-maven-antrun-plugin
BuildRequires:  maven30-maven-dependency-plugin
BuildRequires:  maven30-maven-install-plugin
BuildRequires:  maven30-maven-invoker-plugin
BuildRequires:  maven30-maven-plugin-plugin
BuildRequires:  maven30-maven-plugin-testing-harness
BuildRequires:  maven30-maven-site-plugin
BuildRequires:  maven30-maven-source-plugin
BuildRequires:  maven30-maven-surefire-plugin

BuildRequires:  maven30-ant-antunit
BuildRequires:  %{?scl_prefix_java_common}ant-testutil
BuildRequires:  %{?scl_prefix_java_common}apache-commons-compress


%description
Release Audit Tool (RAT) is a tool to improve accuracy and efficiency when
checking releases. It is heuristic in nature: making guesses about possible
problems. It will produce false positives and cannot find every possible
issue with a release. It's reports require interpretation.

RAT was developed in response to a need felt in the Apache Incubator to be
able to review releases for the most common faults less labor intensively.
It is therefore highly tuned to the Apache style of releases.

This package just contains meta-data, you will want either apache-rat-tasks,
or apache-rat-plugin.


%package core
Summary:        Core functionality for %{pkg_name}
Requires:       %{name} = %{version}-%{release}

%description core
The core functionality of RAT, shared by the Ant tasks, and the Maven plugin.
It also includes a wrapper script "apache-rat" that should be the equivalent
to running upstream's "java -jar apache-rat.jar".


%package plugin
Summary:        Maven plugin for %{pkg_name}
Requires:       %{name}-core = %{version}-%{release}

%description plugin
Maven plugin for running RAT, the Release Audit Tool.


%package tasks
Summary:        Ant tasks for %{pkg_name}
Requires:       %{name}-core = %{version}-%{release}

%description tasks
Ant tasks for running RAT.


%package javadoc
Summary:        Javadocs for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.


%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
%patch0 -p1 -b .doxia-1.1
%patch1 -p1 -b .compat
%patch2 -p1 -b .test

%pom_remove_plugin :maven-antrun-plugin apache-rat-tasks
%pom_xpath_remove pom:extensions

%mvn_package :apache-rat-project apache-rat
%{?scl:EOF}

%build
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
%mvn_build -f -s
%{?scl:EOF}

%install
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
%mvn_install

#Ant taksks
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir_java_common}/ant.d
echo "apache-rat/rat-core apache-rat/rat-tasks" > $RPM_BUILD_ROOT%{_sysconfdir_java_common}/ant.d/%{pkg_name}
%{?scl:EOF}


%files -f .mfiles-apache-rat
%doc DISCLAIMER.txt LICENSE NOTICE README.txt RELEASE_NOTES.txt
%dir %{_mavenpomdir}/%{pkg_name}
%dir %{_javadir}/%{pkg_name}

%files core -f .mfiles-apache-rat-core
%dir %{_mavenpomdir}/%{pkg_name}
%dir %{_javadir}/%{pkg_name}
%doc LICENSE NOTICE

%files plugin -f .mfiles-apache-rat-plugin
%dir %{_mavenpomdir}/%{pkg_name}
%dir %{_javadir}/%{pkg_name}
%doc LICENSE NOTICE

%files tasks -f .mfiles-apache-rat-tasks
%doc LICENSE NOTICE
%dir %{_mavenpomdir}/%{pkg_name}
%dir %{_javadir}/%{pkg_name}
%{_sysconfdir_java_common}/ant.d/%{pkg_name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE


%changelog
* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 0.8-13.18
- maven33 rebuild

* Fri Jan 16 2015 Michal Srb <msrb@redhat.com> - 0.8-13.17
- Fix directory ownership

* Thu Jan 15 2015 Michael Simacek <msimacek@redhat.com> - 0.8-13.16
- Install ant.d files into rh-java-common's ant.d

* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8-13.15
- Add directory ownership on %%{_mavenpomdir} subdir

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 0.8-13.14
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michael Simacek <msimacek@redhat.com> - 0.8-13.13
- Rebuild to regenerate requires from java-common

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 0.8-13.12
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8-13.11
- Mass rebuild 2014-05-26

* Fri Mar 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8-13.10
- Remove wagon-ssh extension from POM

* Thu Feb 20 2014 Michael Simacek <msimacek@redhat.com> - 0.8-13.9
- Remove BR on maven-wagon

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8-13.8
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8-13.7
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8-13.6
- Remove requires on java

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8-13.5
- Add missing BR: maven-plugin-testing-harness

* Fri Feb 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8-13.4
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8-13.3
- Rebuild to regenerate auto-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8-13.2
- Remove %%jpackage_script wrapper

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8-13.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.8-13
- Mass rebuild 2013-12-27

* Tue Aug 27 2013 Michal Srb <msrb@redhat.com> - 0.8-12
- Migrate away from mvn-rpmbuild (Resolves: #997517)

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8-11
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Tue Jun 11 2013 Orion Poplawski <orion@cora.nwra.com> 0.8-10
- Split up depmap fragments (bug 973242)

* Tue Feb 26 2013 Orion Poplawski <orion@cora.nwra.com> 0.8-9
- Drop BR on maven-doxia and maven-doxia-sitetools (bug #915606)

* Tue Feb 12 2013 Orion Poplawski <orion@cora.nwra.com> 0.8-8
- Add apache-rat wrapper script to apache-rat-core (bug #907782)
- Disable tests for now due to Fedora maven bug

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0.8-7
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Aug 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8-6
- Run mvn-rpmbuild package instead of install

* Thu Aug 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8-5
- Install NOTICE files
- Remove defattr

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 7 2011 Orion Poplawski <orion@cora.nwra.com> 0.8-2
- Update to maven 3

* Tue Dec 6 2011 Orion Poplawski <orion@cora.nwra.com> 0.8-1
- Update to 0.8 release
- Add BR maven-invoker-plugin

* Thu Apr 28 2011 Orion Poplawski <orion@cora.nwra.com> 0.8-0.7.20100827
- Add needed requires to core

* Thu Mar 3 2011 Orion Poplawski <orion@cora.nwra.com> 0.8-0.6.20100827
- Drop unneeded rm from %%install
- Don't ship BUILD.txt
- Cleanup Requires

* Mon Dec 27 2010 Orion Poplawski <orion@cora.nwra.com> 0.8-0.5.20100827
- Drop maven settings patch
- Add svn revision to export command
- Set maven.test.failure.ignore=true instead of maven.test.skip
- Use %%{_mavenpomdir}

* Thu Dec 9 2010 Orion Poplawski <orion@cora.nwra.com> 0.8-0.4.20100827
- Change BR to ant-antunit
- Drop versioned jar and javadoc
- Drop BuildRoot and %%clean

* Mon Nov 1 2010 Orion Poplawski <orion@cora.nwra.com> 0.8-0.3.20100827
- Add /etc/ant.d/apache-rat

* Fri Oct 29 2010 Orion Poplawski <orion@cora.nwra.com> 0.8-0.2.20100827
- First real working package

* Wed Aug 11 2010 Orion Poplawski <orion@cora.nwra.com> 0.8-0.1
- Initial Fedora package
