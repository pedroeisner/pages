# No-key FIFA World Cup 2026 calendar generator.
# Generates worldcup2026.ics from a static official schedule skeleton.

from datetime import datetime, timedelta, timezone
from pathlib import Path
import re, uuid

flags = {
'Mexico':'🇲🇽','South Africa':'🇿🇦','South Korea':'🇰🇷','Czech Republic':'🇨🇿','Canada':'🇨🇦','Bosnia and Herzegovina':'🇧🇦','Qatar':'🇶🇦','Switzerland':'🇨🇭',
'Brazil':'🇧🇷','Morocco':'🇲🇦','Haiti':'🇭🇹','Scotland':'🏴','United States':'🇺🇸','Paraguay':'🇵🇾','Australia':'🇦🇺','Turkey':'🇹🇷',
'Germany':'🇩🇪','Curaçao':'🇨🇼','Ivory Coast':'🇨🇮','Ecuador':'🇪🇨','Netherlands':'🇳🇱','Japan':'🇯🇵','Sweden':'🇸🇪','Tunisia':'🇹🇳',
'Belgium':'🇧🇪','Egypt':'🇪🇬','Iran':'🇮🇷','New Zealand':'🇳🇿','Spain':'🇪🇸','Cape Verde':'🇨🇻','Saudi Arabia':'🇸🇦','Uruguay':'🇺🇾',
'France':'🇫🇷','Senegal':'🇸🇳','Iraq':'🇮🇶','Norway':'🇳🇴','Argentina':'🇦🇷','Algeria':'🇩🇿','Austria':'🇦🇹','Jordan':'🇯🇴',
'Portugal':'🇵🇹','DR Congo':'🇨🇩','Uzbekistan':'🇺🇿','Colombia':'🇨🇴','England':'🏴','Croatia':'🇭🇷','Ghana':'🇬🇭','Panama':'🇵🇦'
}

groups = {
'A':['Mexico','South Africa','South Korea','Czech Republic'],
'B':['Canada','Bosnia and Herzegovina','Qatar','Switzerland'],
'C':['Brazil','Morocco','Haiti','Scotland'],
'D':['United States','Paraguay','Australia','Turkey'],
'E':['Germany','Curaçao','Ivory Coast','Ecuador'],
'F':['Netherlands','Japan','Sweden','Tunisia'],
'G':['Belgium','Egypt','Iran','New Zealand'],
'H':['Spain','Cape Verde','Saudi Arabia','Uruguay'],
'I':['France','Senegal','Iraq','Norway'],
'J':['Argentina','Algeria','Austria','Jordan'],
'K':['Portugal','DR Congo','Uzbekistan','Colombia'],
'L':['England','Croatia','Ghana','Panama'],
}

def m(no,date,time,offset,t1,t2,venue,city,stage,group=None,dur=2):
    return dict(no=no,date=date,time=time,offset=offset,t1=t1,t2=t2,venue=venue,city=city,stage=stage,group=group,dur=dur)

events=[]
# Group A
events += [
m(1,'2026-06-11','13:00',-6,'Mexico','South Africa','Estadio Azteca','Mexico City','Group Stage','A'),
m(2,'2026-06-11','20:00',-6,'South Korea','Czech Republic','Estadio Akron','Zapopan','Group Stage','A'),
m(25,'2026-06-18','12:00',-4,'Czech Republic','South Africa','Mercedes-Benz Stadium','Atlanta','Group Stage','A'),
m(28,'2026-06-18','19:00',-6,'Mexico','South Korea','Estadio Akron','Zapopan','Group Stage','A'),
m(53,'2026-06-24','19:00',-6,'Czech Republic','Mexico','Estadio Azteca','Mexico City','Group Stage','A'),
m(54,'2026-06-24','19:00',-6,'South Africa','South Korea','Estadio BBVA','Guadalupe','Group Stage','A'),
]
# B
events += [
m(3,'2026-06-12','15:00',-4,'Canada','Bosnia and Herzegovina','BMO Field / Toronto Stadium','Toronto','Group Stage','B'),
m(8,'2026-06-13','12:00',-7,'Qatar','Switzerland',"Levi's Stadium",'Santa Clara','Group Stage','B'),
m(26,'2026-06-18','12:00',-7,'Switzerland','Bosnia and Herzegovina','SoFi Stadium','Inglewood','Group Stage','B'),
m(27,'2026-06-18','15:00',-7,'Canada','Qatar','BC Place','Vancouver','Group Stage','B'),
m(51,'2026-06-24','12:00',-7,'Switzerland','Canada','BC Place','Vancouver','Group Stage','B'),
m(52,'2026-06-24','12:00',-7,'Bosnia and Herzegovina','Qatar','Lumen Field','Seattle','Group Stage','B'),
]
# C
events += [
m(7,'2026-06-13','18:00',-4,'Brazil','Morocco','MetLife Stadium','East Rutherford','Group Stage','C'),
m(5,'2026-06-13','21:00',-4,'Haiti','Scotland','Gillette Stadium','Foxborough','Group Stage','C'),
m(30,'2026-06-19','18:00',-4,'Scotland','Morocco','Gillette Stadium','Foxborough','Group Stage','C'),
m(29,'2026-06-19','20:30',-4,'Brazil','Haiti','Lincoln Financial Field','Philadelphia','Group Stage','C'),
m(49,'2026-06-24','18:00',-4,'Scotland','Brazil','Hard Rock Stadium','Miami Gardens','Group Stage','C'),
m(50,'2026-06-24','18:00',-4,'Morocco','Haiti','Mercedes-Benz Stadium','Atlanta','Group Stage','C'),
]
# D
events += [
m(4,'2026-06-12','18:00',-7,'United States','Paraguay','SoFi Stadium','Inglewood','Group Stage','D'),
m(6,'2026-06-13','21:00',-7,'Australia','Turkey','BC Place','Vancouver','Group Stage','D'),
m(32,'2026-06-19','12:00',-7,'United States','Australia','Lumen Field','Seattle','Group Stage','D'),
m(31,'2026-06-19','20:00',-7,'Turkey','Paraguay',"Levi's Stadium",'Santa Clara','Group Stage','D'),
m(59,'2026-06-25','19:00',-7,'Turkey','United States','SoFi Stadium','Inglewood','Group Stage','D'),
m(60,'2026-06-25','19:00',-7,'Paraguay','Australia',"Levi's Stadium",'Santa Clara','Group Stage','D'),
]
# E
events += [
m(10,'2026-06-14','12:00',-5,'Germany','Curaçao','NRG Stadium','Houston','Group Stage','E'),
m(9,'2026-06-14','19:00',-4,'Ivory Coast','Ecuador','Lincoln Financial Field','Philadelphia','Group Stage','E'),
m(33,'2026-06-20','16:00',-4,'Germany','Ivory Coast','BMO Field / Toronto Stadium','Toronto','Group Stage','E'),
m(34,'2026-06-20','19:00',-5,'Ecuador','Curaçao','Arrowhead Stadium','Kansas City','Group Stage','E'),
m(55,'2026-06-25','16:00',-4,'Curaçao','Ivory Coast','Lincoln Financial Field','Philadelphia','Group Stage','E'),
m(56,'2026-06-25','16:00',-4,'Ecuador','Germany','MetLife Stadium','East Rutherford','Group Stage','E'),
]
# F
events += [
m(11,'2026-06-14','15:00',-5,'Netherlands','Japan','AT&T Stadium','Arlington','Group Stage','F'),
m(12,'2026-06-14','20:00',-6,'Sweden','Tunisia','Estadio BBVA','Guadalupe','Group Stage','F'),
m(35,'2026-06-20','12:00',-5,'Netherlands','Sweden','NRG Stadium','Houston','Group Stage','F'),
m(36,'2026-06-20','22:00',-6,'Tunisia','Japan','Estadio BBVA','Guadalupe','Group Stage','F'),
m(57,'2026-06-25','18:00',-5,'Japan','Sweden','AT&T Stadium','Arlington','Group Stage','F'),
m(58,'2026-06-25','18:00',-5,'Tunisia','Netherlands','Arrowhead Stadium','Kansas City','Group Stage','F'),
]
# G
events += [
m(16,'2026-06-15','12:00',-7,'Belgium','Egypt','Lumen Field','Seattle','Group Stage','G'),
m(15,'2026-06-15','18:00',-7,'Iran','New Zealand','SoFi Stadium','Inglewood','Group Stage','G'),
m(39,'2026-06-21','12:00',-7,'Belgium','Iran','SoFi Stadium','Inglewood','Group Stage','G'),
m(40,'2026-06-21','18:00',-7,'New Zealand','Egypt','BC Place','Vancouver','Group Stage','G'),
m(63,'2026-06-26','20:00',-7,'Egypt','Iran','Lumen Field','Seattle','Group Stage','G'),
m(64,'2026-06-26','20:00',-7,'New Zealand','Belgium','BC Place','Vancouver','Group Stage','G'),
]
# H
events += [
m(14,'2026-06-15','12:00',-4,'Spain','Cape Verde','Mercedes-Benz Stadium','Atlanta','Group Stage','H'),
m(13,'2026-06-15','18:00',-4,'Saudi Arabia','Uruguay','Hard Rock Stadium','Miami Gardens','Group Stage','H'),
m(38,'2026-06-21','12:00',-4,'Spain','Saudi Arabia','Mercedes-Benz Stadium','Atlanta','Group Stage','H'),
m(37,'2026-06-21','18:00',-4,'Uruguay','Cape Verde','Hard Rock Stadium','Miami Gardens','Group Stage','H'),
m(65,'2026-06-26','19:00',-5,'Cape Verde','Saudi Arabia','NRG Stadium','Houston','Group Stage','H'),
m(66,'2026-06-26','18:00',-6,'Uruguay','Spain','Estadio Akron','Zapopan','Group Stage','H'),
]
# I
events += [
m(17,'2026-06-16','15:00',-4,'France','Senegal','MetLife Stadium','East Rutherford','Group Stage','I'),
m(18,'2026-06-16','18:00',-4,'Iraq','Norway','Gillette Stadium','Foxborough','Group Stage','I'),
m(42,'2026-06-22','17:00',-4,'France','Iraq','Lincoln Financial Field','Philadelphia','Group Stage','I'),
m(41,'2026-06-22','20:00',-4,'Norway','Senegal','MetLife Stadium','East Rutherford','Group Stage','I'),
m(61,'2026-06-26','15:00',-4,'Norway','France','Gillette Stadium','Foxborough','Group Stage','I'),
m(62,'2026-06-26','15:00',-4,'Senegal','Iraq','BMO Field / Toronto Stadium','Toronto','Group Stage','I'),
]
# J
events += [
m(19,'2026-06-16','20:00',-5,'Argentina','Algeria','Arrowhead Stadium','Kansas City','Group Stage','J'),
m(20,'2026-06-16','21:00',-7,'Austria','Jordan',"Levi's Stadium",'Santa Clara','Group Stage','J'),
m(43,'2026-06-22','12:00',-5,'Argentina','Austria','AT&T Stadium','Arlington','Group Stage','J'),
m(44,'2026-06-22','20:00',-7,'Jordan','Algeria',"Levi's Stadium",'Santa Clara','Group Stage','J'),
m(69,'2026-06-27','21:00',-5,'Algeria','Austria','Arrowhead Stadium','Kansas City','Group Stage','J'),
m(70,'2026-06-27','21:00',-5,'Jordan','Argentina','AT&T Stadium','Arlington','Group Stage','J'),
]
# K
events += [
m(23,'2026-06-17','12:00',-5,'Portugal','DR Congo','NRG Stadium','Houston','Group Stage','K'),
m(24,'2026-06-17','20:00',-6,'Uzbekistan','Colombia','Estadio Azteca','Mexico City','Group Stage','K'),
m(47,'2026-06-23','12:00',-5,'Portugal','Uzbekistan','NRG Stadium','Houston','Group Stage','K'),
m(48,'2026-06-23','20:00',-6,'Colombia','DR Congo','Estadio Akron','Zapopan','Group Stage','K'),
m(71,'2026-06-27','19:30',-4,'Colombia','Portugal','Hard Rock Stadium','Miami Gardens','Group Stage','K'),
m(72,'2026-06-27','19:30',-4,'DR Congo','Uzbekistan','Mercedes-Benz Stadium','Atlanta','Group Stage','K'),
]
# L
events += [
m(22,'2026-06-17','15:00',-5,'England','Croatia','AT&T Stadium','Arlington','Group Stage','L'),
m(21,'2026-06-17','19:00',-4,'Ghana','Panama','BMO Field / Toronto Stadium','Toronto','Group Stage','L'),
m(45,'2026-06-23','16:00',-4,'England','Ghana','Gillette Stadium','Foxborough','Group Stage','L'),
m(46,'2026-06-23','19:00',-4,'Panama','Croatia','BMO Field / Toronto Stadium','Toronto','Group Stage','L'),
m(67,'2026-06-27','17:00',-4,'Panama','England','MetLife Stadium','East Rutherford','Group Stage','L'),
m(68,'2026-06-27','17:00',-4,'Croatia','Ghana','Lincoln Financial Field','Philadelphia','Group Stage','L'),
]
# Knockout (published matchup placeholders; no real flags yet)
ko = [
(73,'2026-06-28','12:00',-7,'Runner-up Group A','Runner-up Group B','SoFi Stadium','Inglewood','Round of 32'),
(76,'2026-06-29','12:00',-5,'Winner Group C','Runner-up Group F','NRG Stadium','Houston','Round of 32'),
(74,'2026-06-29','16:30',-4,'Winner Group E','3rd Group A/B/C/D/F','Gillette Stadium','Foxborough','Round of 32'),
(75,'2026-06-29','19:00',-6,'Winner Group F','Runner-up Group C','Estadio BBVA','Guadalupe','Round of 32'),
(78,'2026-06-30','12:00',-5,'Runner-up Group E','Runner-up Group I','AT&T Stadium','Arlington','Round of 32'),
(77,'2026-06-30','17:00',-4,'Winner Group I','3rd Group C/D/F/G/H','MetLife Stadium','East Rutherford','Round of 32'),
(79,'2026-06-30','19:00',-6,'Winner Group A','3rd Group C/E/F/H/I','Estadio Azteca','Mexico City','Round of 32'),
(80,'2026-07-01','12:00',-4,'Winner Group L','3rd Group E/H/I/J/K','Mercedes-Benz Stadium','Atlanta','Round of 32'),
(82,'2026-07-01','13:00',-7,'Winner Group G','3rd Group A/E/H/I/J','Lumen Field','Seattle','Round of 32'),
(81,'2026-07-01','17:00',-7,'Winner Group D','3rd Group B/E/F/I/J',"Levi's Stadium",'Santa Clara','Round of 32'),
(84,'2026-07-02','12:00',-7,'Winner Group H','Runner-up Group J','SoFi Stadium','Inglewood','Round of 32'),
(83,'2026-07-02','19:00',-4,'Runner-up Group K','Runner-up Group L','BMO Field / Toronto Stadium','Toronto','Round of 32'),
(85,'2026-07-02','20:00',-7,'Winner Group B','3rd Group E/F/G/I/J','BC Place','Vancouver','Round of 32'),
(88,'2026-07-03','13:00',-5,'Runner-up Group D','Runner-up Group G','AT&T Stadium','Arlington','Round of 32'),
(86,'2026-07-03','18:00',-4,'Winner Group J','Runner-up Group H','Hard Rock Stadium','Miami Gardens','Round of 32'),
(87,'2026-07-03','20:30',-5,'Winner Group K','3rd Group D/E/I/J/L','Arrowhead Stadium','Kansas City','Round of 32'),
(90,'2026-07-04','12:00',-5,'Winner Match 73','Winner Match 75','NRG Stadium','Houston','Round of 16'),
(89,'2026-07-04','17:00',-4,'Winner Match 74','Winner Match 77','Lincoln Financial Field','Philadelphia','Round of 16'),
(91,'2026-07-05','16:00',-4,'Winner Match 76','Winner Match 78','MetLife Stadium','East Rutherford','Round of 16'),
(92,'2026-07-05','18:00',-6,'Winner Match 79','Winner Match 80','Estadio Azteca','Mexico City','Round of 16'),
(93,'2026-07-06','14:00',-5,'Winner Match 83','Winner Match 84','AT&T Stadium','Arlington','Round of 16'),
(94,'2026-07-06','17:00',-7,'Winner Match 81','Winner Match 82','Lumen Field','Seattle','Round of 16'),
(95,'2026-07-07','12:00',-4,'Winner Match 86','Winner Match 88','Mercedes-Benz Stadium','Atlanta','Round of 16'),
(96,'2026-07-07','13:00',-7,'Winner Match 85','Winner Match 87','BC Place','Vancouver','Round of 16'),
(97,'2026-07-09','16:00',-4,'Winner Match 89','Winner Match 90','Gillette Stadium','Foxborough','Quarter-finals'),
(98,'2026-07-10','12:00',-7,'Winner Match 93','Winner Match 94','SoFi Stadium','Inglewood','Quarter-finals'),
(99,'2026-07-11','17:00',-4,'Winner Match 91','Winner Match 92','Hard Rock Stadium','Miami Gardens','Quarter-finals'),
(100,'2026-07-11','20:00',-5,'Winner Match 95','Winner Match 96','Arrowhead Stadium','Kansas City','Quarter-finals'),
(101,'2026-07-14','14:00',-5,'Winner Match 97','Winner Match 98','AT&T Stadium','Arlington','Semi-finals'),
(102,'2026-07-15','15:00',-4,'Winner Match 99','Winner Match 100','Mercedes-Benz Stadium','Atlanta','Semi-finals'),
(103,'2026-07-18','17:00',-4,'Loser Match 101','Loser Match 102','Hard Rock Stadium','Miami Gardens','Third-place play-off'),
(104,'2026-07-19','15:00',-4,'Winner Match 101','Winner Match 102','MetLife Stadium','East Rutherford','Final'),
]
events += [m(*x, group=None, dur=3) for x in ko]

def esc(s):
    return str(s).replace('\\','\\\\').replace('\n','\\n').replace(';','\\;').replace(',','\\,')

def fold(line):
    # simple character folding; OK for modern calendars
    out=[]
    while len(line)>73:
        out.append(line[:73])
        line=' '+line[73:]
    out.append(line)
    return '\r\n'.join(out)

def dt_utc(date,time,offset):
    local=datetime.fromisoformat(date+'T'+time+':00')
    tz=timezone(timedelta(hours=offset))
    return local.replace(tzinfo=tz).astimezone(timezone.utc)

def summary(e):
    def side(t):
        return f"{flags.get(t,'🏆')} {t}" if (t in flags) else t
    return f"{side(e['t1'])} - {side(e['t2'])}"

def desc(e):
    parts=[f"Stage: {e['stage']}", f"Match: {e['no']}"]
    if e.get('group'):
        teams=', '.join(groups[e['group']])
        parts.append(f"Group: Group {e['group']}")
        parts.append(f"Group teams: {teams}")
    return '\n'.join(parts)

lines=['BEGIN:VCALENDAR','VERSION:2.0','CALSCALE:GREGORIAN','METHOD:PUBLISH','PRODID:-//OpenAI//FIFA World Cup 2026 Custom Calendar//EN','X-WR-CALNAME:FIFA World Cup 2026','X-WR-TIMEZONE:UTC']
now=datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
for e in sorted(events, key=lambda x: (x['date'], x['time'], x['no'])):
    start=dt_utc(e['date'], e['time'], e['offset'])
    end=start+timedelta(hours=e['dur'])
    uid=f"fifa-world-cup-2026-match-{e['no']}@openai.local"
    loc=f"{e['venue']}, {e['city']}"
    for line in ['BEGIN:VEVENT',f'UID:{uid}',f'DTSTAMP:{now}',f'DTSTART:{start.strftime("%Y%m%dT%H%M%SZ")}',f'DTEND:{end.strftime("%Y%m%dT%H%M%SZ")}',f'SUMMARY:{esc(summary(e))}',f'LOCATION:{esc(loc)}',f'DESCRIPTION:{esc(desc(e))}', 'STATUS:CONFIRMED','TRANSP:OPAQUE','END:VEVENT']:
        lines.append(fold(line))
lines.append('END:VCALENDAR')
Path('worldcup2026.ics').write_text('\r\n'.join(lines)+'\r\n', encoding='utf-8')
print(f"Wrote worldcup2026.ics with {len(events)} events")
