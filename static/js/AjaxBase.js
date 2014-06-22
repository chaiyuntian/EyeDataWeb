
function initChannel () {
  function XHR(url, method, options) {
    options=options||XHR.createOptions('json','application/json',false,true);
    var xhr=new XMLHttpRequest();
    this.defer = options.defer|Object.defer();
    this.xhr = xhr;
    this.responseType = options.responseType;
    xhr.onreadystatechange = this.xhrStateChange.bind(this, xhr);
    xhr.onerror = this.xhrError.bind(this, xhr);
    this.contentType = options.contentType;
    this.withCredentials = options.withCredentials;
    this.startTime = this.endTime = null;
    this.notifyLoading = options.notifyLoading;
    this.url = url;
    this.method = method || 'get';
  }
  XHR.prototype = {
    _getCallBacks: function () {
      var cbs = this._callbacks;
      if (!cbs)this._callbacks = cbs = {};
      return cbs;
    },
    xhrError: function (xhr, error) {
      this.endTime = Date.now();
      this.emit('error',[xhr,error]);
    },
    abort: function () {
      this.xhr.abort();
      this.emit('abort',[this.xhr]);
    },
    xhrStateChange: function (xhr) {
      switch (xhr.readyState) {
        case 1://XMLHttpRequest.OPENED:
          xhr.responseType = this.responseType;
          xhr.overrideMimeType(this.contentType);
          xhr.setRequestHeader("Content-Type",this.contentType+';charset=UTF-8');
          xhr.withCredentials = this.withCredentials;
          this.emit('opened', [xhr]);
          break;
        case 2://XMLHttpRequest.HEADERS_RECEIVED:
          this.emit('headers', [xhr]);
          break;
        case 3://loading
          if (this.notifyLoading)
            this.emit('loading', [xhr]);
          break;
        case 4:
          if (xhr.status == 200)
            this.emit('success',[xhr]);
          else
            this.emit('fail',[xhr]);
          this.emit('done',[xhr]);
          break;
      }
    },
    _autoSend: function () {
      this.send()
    },
    get promise() {
      return this.defer.promise;
    },
    get timeUsed() {
      return (this.endTime || Date.now() - this.startTime) / 1000 || undefined;
    },
    get timeOut() {
      return this._timeOut;
    },
    set timeOut(t) {
      if (t < 0 || isNaN(t))return;
      this._timeOut = t;
    },
    get isSent(){
      return this.xhr.readyState>1;
    },
    setQuery:function(key,value){
      var q=this.query;
      if(!q)this.query=q={};
      q[key]=value;
      return this;
    },
    get queryString(){
      var q=this.query,keys;
      if(!q)return '';
      keys=Object.getOwnPropertyNames(q);
      if(!keys.length)return'';
      for(var i= 0,key=keys[i],str='?';key;key=keys[++i])
       str+=(encodeURIComponent(key)+'='+encodeURIComponent(q[key])+'&');
      return str.substring(0,str.length-1);
    },
    open: function (onOpened) {
      if(typeof onOpened =="function") this.on('opened',onOpened);
      this.xhr.open(this.method,this.url+this.queryString);
      return this;
    },
    send: function (data) {
      if (data !== undefined)this.data = data;
      switch (this.xhr.readyState) {
        case 0:
          this.open(this._autoSend);
          break;
        case 1:
          this.startTime = Date.now();
          this.xhr.send(this.data || null);
          break;
      }
      return this;
    }
  };
  XHR.createOptions=function(resType,contentType,notifyLoading,withCredentials){
    return {
      responseType:resType,
      contentType:contentType,
      withCredentials:withCredentials,
      notifyLoading:notifyLoading
    };
  };
  var exporter={
    createXHR:
      function(url, method, options){
        return new XHR(url,method,options);
      },
    XHROption:XHR.createOptions
  };
  initChannel=undefined;
  return exporter;
}
