import channel
import pymetar


class Weather(channel.Channel):

  def SetUp(self):
    print 'Weather Channel'
    print 'ICAO:',
    self.icao = str(raw_input())

  def Display(self):
    fetcher = pymetar.ReportFetcher()
    report = fetcher.FetchReport(self.icao)
    parser = pymetar.ReportParser()
    parser.ParseReport(report)
    temperature = report.getTemperatureCelsius()
    # NOTE(damonkohler): There is no 'Weather' heading for clear weather.
    weather = report.getWeather() or 'Clear'
    self.pert.Clear()
    self.pert.WrapMessage('%d\xdfC %s' % (temperature, weather))
