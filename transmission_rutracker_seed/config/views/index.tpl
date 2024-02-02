<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ _('Configuration') }}</title>
  <link rel="stylesheet" href="/static/bootstrap/css/bootstrap.min.css">
  <link rel="stylesheet" href="/static/bootstrap/css/bootstrap-theme.min.css">
</head>
<body>
  <script type="text/javascript">
    function refresh_useragent() {
      user_agent.value = window.navigator.userAgent
    }
  </script>
  <div class="container">
  <h1>{{ _('Configuration') }}</h1><br>
    <div class="row" style="background-color: #eee;">
      <div class="col-sm-12">
        <form class="form-horizontal" action="/save/transmission" method="POST">
          <div class="form-group">
            <div class="col-sm-12">
              <h3>Transmission</h3>
            </div>
          </div>
          <div class="form-group">
            <label for="protocol" class="col-sm-2 control-label">{{ _('protocol') }}</label>
            <div class="col-sm-2">
              <select class="form-control" id="protocol" name="protocol">
                <option {{ 'selected=selected' if transmission.protocol is None or transmission.protocol == 'http' else '' }} >http</option>
                <option {{ 'selected=selected' if transmission.protocol == 'https' else '' }}>https</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label for="username" class="col-sm-2 control-label">{{ _('username') }}</label>
            <div class="col-sm-10">
              <input class="form-control" type="text" id="username" name="username" value="{{transmission.username or ''}}">
            </div>
          </div>
          <div class="form-group">
            <label for="password" class="col-sm-2 control-label">{{ _('password') }}</label>
            <div class="col-sm-10">
              <input class="form-control" type="password" id="password" name="password" value="{{transmission.password or ''}}">
            </div>
          </div>
          <div class="form-group">
            <label for="host" class="col-sm-2 control-label">{{ _('host') }}</label>
            <div class="col-sm-10">
              <input class="form-control" type="text" id="host" name="host" value="{{transmission.host or ''}}">
            </div>
          </div>
          <div class="form-group">
            <label for="port" class="col-sm-2 control-label">{{ _('port') }}</label>
            <div class="col-sm-10">
              <input class="form-control" type="number" id="port" name="port" value="{{transmission.port or ''}}">
            </div>
          </div>
          <div class="form-group">
            <label for="path" class="col-sm-2 control-label">{{ _('path') }}</label>
            <div class="col-sm-10">
              <input class="form-control" type="url" id="path" name="path" value="{{transmission.path or ''}}">
            </div>
          </div>
          <div class="form-group">
            <div class="col-sm-offset-2 col-sm-10">
              <button type="submit" class="btn btn-default">{{ _('Save') }}</button>
            </div>
          </div>
        </form>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-12">
        <form class="form-horizontal" action="/save/browser" method="POST">
          <div class="form-group">
            <div class="col-sm-12">
              <h3>{{ _('Browser') }}</h3>
            </div>
          </div>
          <div class="form-group">
            <label for="user_agent" class="col-sm-2 control-label">{{ _('User Agent') }}</label>
            <div class="col-sm-8">
              <input class="form-control" type="text" id="user_agent" name="user_agent" aria-describedby="user_agent_help" value="{{browser.user_agent or ''}}">
              <span id="user_agent_help" class="help-block">{{ _('Used to cheat CloudFlare and rutracker.org') }}</span>
            </div>
            <div class="col-sm-2">
              <button type="button" onclick="refresh_useragent()" class="btn btn-default">{{ _('Refresh') }}</button>
            </div>
          </div>
          <div class="form-group">
            <label for="debug_http" class="col-sm-2 control-label">{{ _('debug') }}</label>
            <div class="col-sm-2">
              <select class="form-control" id="debug_http" name="debug_http">
                <option {{ 'selected=selected' if not browser.debug_http else '' }} value="false">{{ _('false') }}</option>
                <option {{ 'selected=selected' if browser.debug_http else ''}} value="true">{{ _('true') }}</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <div class="col-sm-offset-2 col-sm-10">
              <button type="submit" class="btn btn-default">{{ _('Save') }}</button>
            </div>
          </div>
        </form>
      </div>
    </div>
    <div class="row" style="background-color: #eee;">
      <div class="col-sm-12">
        <form class="form-horizontal" action="/save/browser_cookies" method="POST">
          <div class="form-group">
            <div class="col-sm-12">
              <h3>{{ _('Authentication cookies') }}</h3>
            </div>
          </div>
          <div class="form-group">
            <label for="bb_t" class="col-sm-2 control-label">bb_t</label>
            <div class="col-sm-10">
              <textarea class="form-control" rows="10" id="bb_t" name="bb_t">{{browser_cookies.bb_t or ''}}</textarea>
            </div>
          </div>
          <div class="form-group">
            <label for="bb_ssl" class="col-sm-2 control-label">bb_ssl</label>
            <div class="col-sm-10">
              <input class="form-control" type="text" id="bb_ssl" name="bb_ssl" value="{{browser_cookies.bb_ssl or ''}}">
            </div>
          </div>
          <div class="form-group">
            <label for="bb_session" class="col-sm-2 control-label">bb_session</label>
            <div class="col-sm-10">
              <input class="form-control" type="text" id="bb_session" name="bb_session" value="{{browser_cookies.bb_session or ''}}">
            </div>
          </div>
          <div class="form-group">
            <div class="col-sm-offset-2 col-sm-10">
              <button type="submit" class="btn btn-default">{{ _('Save') }}</button>
            </div>
          </div>
        </form>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-12">
        <form class="form-horizontal" action="/save/logging" method="POST">
          <div class="form-group">
            <div class="col-sm-12">
              <h3>{{ _('Logging') }}</h3>
            </div>
          </div>
          <div class="form-group">
            <label for="level" class="col-sm-2 control-label">{{ _('level') }}</label>
            <div class="col-sm-2">
              <select class="form-control" id="level" name="level" aria-describedby="logging_level_help">
                <option {{ 'selected=selected' if logging.level == 'DEBUG' else '' }} value="DEBUG">{{ _('DEBUG') }}</option>
                <option {{ 'selected=selected' if logging.level == 'INFO' else '' }} value="INFO">{{ _('INFO') }}</option>
                <option {{ 'selected=selected' if logging.level == 'WARNING' else '' }} value="WARNING">{{ _('WARNING') }}</option>
                <option {{ 'selected=selected' if logging.level == 'ERROR' else '' }} value="ERROR">{{ _('ERROR') }}</option>
                <option {{ 'selected=selected' if logging.level == 'CRITICAL' else '' }} value="CRITICAL">{{ _('CRITICAL') }}</option>
              </select>
            </div>
            <span id="logging_level_help" class="help-block">
              {{ _('Show messages this level and higher') }}.
              {{ _('DEBUG') }} < {{ _('INFO') }} < {{ _('WARNING') }} < {{ _('ERROR') }} < {{ _('CRITICAL') }}
            </span>
          </div>
          <div class="form-group">
            <div class="col-sm-offset-2 col-sm-10">
              <button type="submit" class="btn btn-default">{{ _('Save') }}</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</body>
</html>
