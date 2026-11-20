"""Build the Codex guide from the canonical Claude methodology and Codex setup text.
Run from any directory: python scripts/build_lavri_cut.py (requires beautifulsoup4).
Shared FAQ source: assets/lavri-cut/faq.json. Update instructions have one canonical page.
"""
from pathlib import Path
from copy import deepcopy
import html,json
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1]
claude_path=R/'guides/lavri-cut/index.html'
s=BeautifulSoup(claude_path.read_text(),'html.parser')
faq=json.loads((R/'assets/lavri-cut/faq.json').read_text())
faqhtml='<h2>Работа, файлы и обновления</h2><div class="qa" data-shared-faq="1">'+''.join('<details><summary>'+html.escape(q)+'</summary><div><p>'+html.escape(a)+'</p></div></details>' for q,a in faq)+'</div>'
# Refresh the common FAQ in the canonical source as well.
old=s.select_one('[data-shared-faq]');replacement=BeautifulSoup(faqhtml,'html.parser')
if old:
 old.replace_with(replacement.select_one('[data-shared-faq]'))
s.body['data-platform']='claude'
if not s.noscript:s.head.append(BeautifulSoup('<noscript><style>.page{display:block}</style></noscript>','html.parser'))
claude_path.write_text(str(s))
c=BeautifulSoup(str(s),'html.parser');c.body['data-platform']='codex'
c.title.string='ChatGPT: подключение монтажного агента LAVRI Cut к Codex · LAVRI LOOK'
c.select_one('meta[name=description]')['content']='LAVRI Cut в Codex: установка на компьютер и в облако, первый ролик, редактор, звуки, распаковка, анализ конкурентов, правки и общая инструкция обновления.'
for link in c.select('.platform-links a'):
 link.attrs.pop('aria-current',None)
 if link.get('href')=='../lavri-cut-codex/':link['aria-current']='page'
for link in c.select('a[href*="lavri-cut-update/"]'):link['href']='../lavri-cut-update/?platform=codex'
# Shared work sections are derived from the canonical Claude page, rather than edited independently.
for id in ['p-first','p-editor','p-more','p-unpack','p-comp','p-edits','p-get','p-home']:
 el=c.find(id=id)
 for image in list(el.select('figure')):image.decompose() # Claude screens must never be presented as Codex.
 text=str(el).replace('CLAUDE.md','AGENTS.md и CLAUDE.md')
 text=text.replace('обычный чат Claude','обычный чат ChatGPT').replace('к Claude','к выбранной платформе')
 text=text.replace('Виртуальный компьютер Claude','Рабочая среда Codex').replace('Свой монтажёр Reels в Claude','Свой монтажёр Reels в Codex')
 text=text.replace('Монтажный агент LAVRI Cut · Claude','Монтажный агент LAVRI Cut · Codex')
 text=text.replace('Субтитры: 13 стилей в базе','Субтитры под ваш образ').replace('48 звуковых эффектов в базе','Библиотека звуковых эффектов').replace('48 звуковых эффектов','Библиотека звуковых эффектов').replace('13 вариантов','варианты вашей версии').replace('13 стилей','набор стилей')
 text=text.replace('48 звуков, шрифты','звуки, шрифты')
 text=text.replace('Агент сам найдёт подходящие вставки, покажет лист с номерами и скачает выбранные.','Если доступ к поиску и скачиванию есть в текущей сессии, агент покажет подборку и скачает выбранные вставки.')
 el.replace_with(BeautifulSoup(text,'html.parser'))
# Codex-specific overview and limitations, while retaining all work methodology.
c.select_one('#p-home .lead').string='Готовый монтажный агент по авторской методике LAVRI: работа с речью, паузами, субтитрами, плашками, звуком и правками. Сначала установите свой пакет в рабочую папку или репозиторий Codex. Обычный чат ChatGPT сам по себе агент не подключает.'
for a in c.select('#p-home .choice'):
 tag=a.select_one('.tag')
 if tag:tag.string='Локальная установка' if a['href']=='#pc' else 'Облако · компьютер и телефон'
for p in c.select('#p-home p'):
 if 'это проще всего' in p.get_text():p.string='Выбирайте компьютер для локальной работы с файлами или облако для доступа с разных устройств. Проверьте возможности своего тарифа и среды; наличие Codex не означает, что пакет уже установлен.'
# No verified package was supplied for this platform; do not freeze counts or guarantee future interfaces.
c.select_one('#p-home .feat').insert_after(BeautifulSoup('<p class="note">Доступные стили, звуки, шрифты и элементы редактора агент проверяет по вашему архиву. Описание возможностей не заменяет проверку установленной версии. Внешние источники и коннекторы доступны только при реальном подключении и подходящих разрешениях.</p>','html.parser'))
# Remove Claude environment instructions from Codex stock section; retain the general methodology.
pix=c.find(id='pixabay')
for h in list(pix.select('h3')):
 if h.get_text()=='В облаке':
  nxt=h.find_next_sibling('p');nxt.clear();nxt.append(BeautifulSoup('Добавьте ключ в защищённые Secrets / переменные среды Codex по правилам своего клиента. Не вставляйте секрет в чат, код или Git. Попросите агента проверить только наличие переменной, не её значение. После сохранения настроек запустите задачу с обновлённой средой.','html.parser'))
# Codex editor themes are editor-only; all actual fields are version-dependent.
c.select_one('#p-editor .step').insert(2,BeautifulSoup('<p>Для Codex предусмотрены серое, тёмное и светлое оформления редактора. Доступные темы и элементы проверьте в своём пакете; они не меняют оформление этой инструкции.</p>','html.parser'))
c.select_one('#p-editor .next').insert_before(BeautifulSoup('<p class="note">В облаке сначала попросите агента проверить способ открытия редактора: доступный предпросмотр, публикуемая ссылка или другой инструмент сессии. Адрес localhost работает на том компьютере, где запущен сервер, и не является ссылкой для телефона.</p>','html.parser'))
# Preserve Claude-specific FAQ only on Claude; Codex gets its own setup questions plus the common base.
help=c.find(id='p-help');teach=deepcopy(help.find(id='teach'))
help.clear();help.append(BeautifulSoup('<div class="hero"><p class="kicker">Помощь · Codex</p><h1>Частые вопросы</h1><p class="lead">Напишите, на каком шаге остановились, и передайте текст ошибки без ключей и паролей. Агент сначала проверяет причину и доступные инструменты.</p></div>','html.parser'));help.append(teach)
custom=[('Я написала промпт в ChatGPT, но агент не появился','Откройте Codex, выберите свою рабочую папку на компьютере или подключённый репозиторий в облаке и передайте архив. Сам текст запроса в обычном чате не создаёт доступ к файлам.'),('Что выбрать на Windows или Mac?','Для Codex CLI используйте актуальную установку из официального репозитория OpenAI. Если предпочитаете приложение Codex, проверьте поддержку своей ОС на странице загрузки. В клиенте нужен доступ к выбранной папке; облачный Codex — отдельная среда.'),('Не проходят doctor или demo','Сохраните полный текст ошибки и попросите проверить зависимости, браузер, распознавание речи, сеть и настройки пакета по docs/setup-codex.md. Не создавайте движок заново и не удаляйте неизвестные файлы.'),('Что если закончились лимиты?','Попросите сохранить код, план, правила и текущий статус в своей рабочей ветке. Отдельно скачайте нужные файлы из временной облачной среды. Продолжайте с сохранённого шага, когда доступ восстановится.'),('Как подключить Google Диск, Higgsfield или Metricool?','Возможности обычного ChatGPT и Codex могут различаться. Попросите проверить инструменты именно текущей сессии и доступ к нужному действию. Если коннектора нет, передайте исходник доступным способом. Платные генерации и сервисы — только с вашего согласия.')]
help.append(BeautifulSoup('<h2>Установка и доступ</h2><div class="qa">'+''.join('<details><summary>'+html.escape(q)+'</summary><div><p>'+html.escape(a)+'</p></div></details>' for q,a in custom)+'</div>'+faqhtml+'<div class="cta-line"><span>Не получилось — разберём конкретный шаг.</span><a class="btn" href="https://t.me/lavri_ai">Поддержка →</a></div><div class="next"><a class="btn ghost" href="#edits">← Как просить правку</a><a class="btn" href="#get">Получить агента →</a></div>','html.parser'))
# The shared setup request is stored once, then rendered in full for copying.
request=(R/'assets/lavri-cut/codex-install.txt').read_text()
def box(title,text):return '<div class="copybox"><div class="head">'+title+'<button class="copy" type="button">Скопировать</button></div><pre>'+html.escape(text)+'</pre></div>'
pc='''<div class="hero"><p class="kicker">Codex на компьютере</p><h1>Установка на компьютер</h1><p class="lead">Ваш персональный ZIP, отдельная рабочая папка и Codex с доступом к файлам и командам. Код агента уже готов — писать его заново не нужно.</p></div>
<div class="step" id="pc-need"><span class="num">Перед началом</span><h2>Что понадобится</h2><ul><li>Компьютер, доступ к интернету и место для видео, моделей и зависимостей.</li><li>Codex: приложение для поддерживаемой ОС или CLI (си-эл-ай, работа через терминал). Проверьте доступ в своём тарифе ChatGPT либо отдельно настроенную авторизацию.</li><li>Ваш архив LAVRI Cut для Codex. Если пакет был выдан для Claude, сначала уточните у автора совместимость и получение варианта Codex.</li><li>Отдельная папка или репозиторий. Установку Claude не заменяем.</li></ul></div>
<div class="step" id="pc-1"><span class="num">Шаг 1</span><h2>Установите Codex и войдите</h2><p>Откройте <a href="https://chatgpt.com/codex?app-landing-page=true">официальную страницу приложения Codex</a> и проверьте поддержку своей ОС. Если выбираете терминал, следуйте <a href="https://github.com/openai/codex#quickstart">официальной инструкции Codex CLI</a>: в ней отдельно описаны Mac / Linux и Windows. Установка Codex ещё не устанавливает LAVRI Cut.</p><p>При уже установленном Node.js один из официальных способов установки CLI:</p>'''+box('Codex CLI · установка','npm install -g @openai/codex')+'''<p>После установки запустите <code>codex</code> и выберите <b>Sign in with ChatGPT</b> (сайн ин уиз чат-джи-пи-ти, вход через ChatGPT). Пароль вводится в окне авторизации, не в чате. Доступ по API настраивается отдельно и может иметь отдельную оплату.</p></div>
<div class="step" id="pc-2"><span class="num">Шаг 2</span><h2>Выберите свою папку</h2><p>Создайте отдельную папку, например <code>Montage-Codex</code>. В приложении откройте её как проект; в CLI перейдите в эту папку командой <code>cd</code> с вашим путём, затем запустите <code>codex</code>. Проверьте, что в задаче указана именно эта папка.</p><p>Положите ZIP в доступное место и сообщите полный путь к нему. Если клиент поддерживает прикрепление архива, можно использовать его; одинаковой кнопки во всех клиентах нет. Архив сначала распаковывается во временную папку для проверки.</p></div>
<div class="step" id="pc-3"><span class="num">Шаг 3</span><h2>Отправьте запрос установки</h2><p>Укажите путь к архиву перед запросом ниже. Агент читает правила и docs/setup-codex.md из вашего пакета, создаёт точку возврата и рабочую ветку, сохраняет наработки и добавляет только недостающие зависимости. Если папка ещё не является Git-репозиторием, сначала попросите подготовить локальный репозиторий для рабочей ветки. Системный пароль вводите самостоятельно в окне системы.</p><a class="btn" href="#install-request">Открыть полный запрос установки →</a></div>
<div class="step" id="pc-4"><span class="num">Шаг 4</span><h2>Проверьте демо и скачивание</h2><p>Дождитесь результатов <code>npm run doctor</code> и <code>npm run demo</code>, отчёта технической приёмки и настоящего тестового MP4. Откройте редактор доступным способом и скачайте полный файл. Проверьте, что он воспроизводится на вашем компьютере. При ошибке сохраните сообщение и точку возврата.</p></div><div class="next"><a class="btn ghost" href="#home">← Что внутри</a><a class="btn" href="#first">Первый ролик →</a></div>'''
cloud='''<div class="hero"><p class="kicker">Codex в облаке · компьютер и телефон</p><h1>Установка в облако</h1><p class="lead">Код и правила сохраняются в вашем приватном репозитории. Монтаж выполняется в облачной рабочей среде Codex; обычный чат не заменяет её подключение.</p></div>
<div class="step" id="cl-1"><span class="num">Шаг 1</span><h2>Создайте отдельный репозиторий</h2><p>На <a href="https://github.com/new">GitHub</a> создайте приватный репозиторий, например <code>montage-codex</code>, с README. Если агент Claude уже установлен в другом репозитории, оставьте его без изменений. Клиентский архив, исходники и секреты в публичный репозиторий не загружайте.</p></div>
<div class="step" id="cl-2"><span class="num">Шаг 2</span><h2>Подключите GitHub к Codex</h2><p>Откройте <a href="https://chatgpt.com/codex">Codex</a>, войдите в свой аккаунт и настройте подключение GitHub. Разрешите доступ к нужному репозиторию и выберите его в новой задаче. Если он не виден, проверьте аккаунт, доступ интеграции и список разрешённых репозиториев. Промпт не может выдать себе доступ.</p><p>На телефоне используйте доступный в вашем аккаунте облачный интерфейс Codex. Сначала убедитесь, что выбран тот же репозиторий и рабочая среда.</p></div>
<div class="step" id="cl-3"><span class="num">Шаг 3</span><h2>Проверьте рабочую среду</h2><p>Откройте настройки среды своего репозитория. Попросите агента проверить текущие зависимости, браузер, кэш моделей, доступ к пакетам и разрешённые домены по <code>docs/setup-codex.md</code> актуального ZIP. Готовые настройки повторять не нужно.</p><p>Для монтажа обычно нужны Node.js и зависимости пакета, FFmpeg, Python, браузер для сборки и доступ к модели распознавания речи. Точные версии, команды и домены определяются вашим пакетом. Для Диска, стоков, шрифтов и генераторов нужен доступ к соответствующим источникам. Список среды Claude не копируйте автоматически в Codex.</p><p>Если инструменты настройки доступны агенту, он подготовит недостающее. Если нужны ваши действия в интерфейсе — например, сохранить или опубликовать среду, — он должен указать конкретный шаг. Подготовленный черновик ещё не означает, что настройки применены. Секреты вводятся только в защищённые настройки среды.</p></div>
<div class="step" id="cl-5"><span class="num">Шаг 4</span><h2>Передайте архив и запустите установку</h2><p>В выбранной задаче передайте ZIP поддерживаемым способом либо проверенную ссылку, которую агент действительно может скачать. Если прикрепление не поддерживается, попросите назвать доступный способ передачи файла. Публичную ссылку на персональный архив создавать не нужно.</p><p>Отправьте запрос ниже целиком. Агент переносит содержимое корневой папки пакета в корень выбранного репозитория, без двойной вложенности, сохраняет номер и авторство, создаёт точку возврата и отдельную ветку Codex.</p></div>
<div class="step" id="install-request"><span class="num">Полный запрос · компьютер и облако</span><h2>Установка LAVRI Cut в Codex</h2>'''+box('Готовый запрос установки',request)+'''<p><a href="../../assets/lavri-cut/codex-install.txt" download>Скачать запрос TXT</a></p></div>
<div class="step" id="cl-6"><span class="num">Шаг 5</span><h2>Демо, редактор и настоящий MP4</h2><p>Проверьте отчёт doctor / demo и техническую приёмку. Попросите открыть редактор реально доступным в сессии способом. Внутренний localhost облачной среды не является внешней ссылкой. Если предпросмотр недоступен, агент должен назвать ограничение и альтернативу.</p><p>Для скачивания нужен отдельный настоящий MP4 с проверенными форматом, размером и SHA256 (ша-двести-пятьдесят-шесть, контрольная сумма файла). Откройте его на своём телефоне: проверка в среде не подтверждает скачивание на устройство.</p><p>Если выдача организована через отдельную ветку <code>delivery</code> (деливери, выдача файлов) вашего репозитория, открывайте прямую ссылку с авторизацией GitHub. Это один из вариантов, доступность которого агент проверяет в текущей сессии; код и клиентские файлы не должны становиться публичными.</p></div>
<div class="step" id="cl-9"><span class="num">Шаг 6</span><h2>Следующая задача — в том же проекте</h2><p>После успешной установки проверьте, что код и правила сохранены в рабочей ветке. Следующую задачу начинайте в том же репозитории с установленным агентом. Попросите прочитать правила и сохранённый статус. Код, стили и память сохраняйте в репозитории, а большие исходники и готовые ролики — отдельно: временная сессия не является архивом.</p><p>До первого монтажа настройте свой образ: приложите примеры шрифтов, цветов, музыки и Reels. Коннекторы проверяйте на конкретном действии: прочитать файл, скачать исходник или загрузить результат.</p></div><div class="cta-line"><span>Нужна помощь с подключением?</span><a class="btn ghost" href="https://t.me/lavri_ai">Получить консультацию →</a></div><div class="next"><a class="btn ghost" href="#home">← Что внутри</a><a class="btn" href="#first">Первый ролик →</a></div>'''
for id,body in [('p-pc',pc),('p-cloud',cloud)]:
 el=c.find(id=id);el.clear();el.append(BeautifulSoup(body,'html.parser'))
# Make the canonical page heading explicit, without changing the shared section headings.
c.select_one('#p-home h1').string='ChatGPT: подключение монтажного агента LAVRI Cut к Codex'
c.select_one('#p-get .lead').string='Получите персональный архив через существующий процесс автора и установите в отдельный проект Codex. Если архив выдан для другой платформы, уточните совместимость в поддержке.'
# Shared work section cross-links must not target Claude-only anchors.
for link in c.select('a[href="#cl-domains"]'):link['href']='#cl-3'
for link in c.select('a[href="#pc-2"]'):link['href']='#pc-2'
# All remaining images in the copied document belong to removed setup/help sections; none should remain.
assert not c.select('img'), 'Do not publish Claude screenshots as Codex'
footer=c.select_one('footer')
if footer:footer.insert_before(BeautifulSoup('<p class="sources wrap">Установка Codex: <a href="https://github.com/openai/codex#quickstart">официальный репозиторий OpenAI</a> · <a href="https://developers.openai.com/codex/cloud/environments/">облачные среды</a>. Способы входа и состав интерфейса зависят от клиента и доступных настроек.</p>','html.parser'))
p=R/'guides/lavri-cut-codex';p.mkdir(exist_ok=True);(p/'index.html').write_text(str(c))
print('Built canonical Codex guide from shared Claude methodology and current setup request')
