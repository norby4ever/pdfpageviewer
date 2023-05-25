Summary:	Welcome pages for M OS
Summary(ru_RU.UTF-8): Приветственный PDF-файл для М ОС
Name:		welcome-pages
Version:	1.0
Release:	1
License:	GPLv3
Group:		System/Configuration/Other
Url:		https://github.com/norby4ever/pdfpageviewer
Source1:	main.py
Source2:	welcome-pages.desktop

Requires:	python3-qtpy
Requires:	python3-qpageview
Requires:	python3-poppler-qt5

BuildArch:	noarch

%description
Shows welcome PDF-file when system runs the first time, allows enable sending anonymous statistics

%description -l ru_RU.UTF-8
Показывает PDF файл при первом старте системы, предоставляет возможность включить отправку анонимной статистики

%files
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/__pycache__
%{_datadir}/%{name}/main.py
%{_sysconfdir}/.config/autostart/welcome-pages.desktop
%{_bindir}/%{name}

#------------------------------------------------------------------

%prep
%setup -T -c
cp %sources .

%build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/%{name}
install -m755 main.py %{buildroot}%{_datadir}/%{name}/main.py
ln -s ../share/%{name}/main.py %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/.config/autostart
install -m644 welcome-pages.desktop %{buildroot}%{_sysconfdir}/.config/autostart/welcome-pages.desktop
