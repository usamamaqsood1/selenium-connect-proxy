import os
import time
import zipfile
from selenium import webdriver

PROXY_HOST = 'Host'
PROXY_PORT = 11603  # add you port
PROXY_USER = 'username'
PROXY_PASS = 'password'

manifest_json = '''
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Undetectable",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking",
        "privacy",
        "storage",
        "activeTab"
    ],
    "background": {
        "scripts": ["background.js"]
    },

    "browser_action": {
    "browser_style": false,
    "default_title": "Your IP is visible"
    },
    "minimum_chrome_version": "22.0.0"
}



'''

background_js = '''

var proxyConfig = {
    mode: "fixed_servers",
    rules: {
        singleProxy: {
            scheme: "http",
            host: "%s", // Replace with your proxy host
            port: parseInt(%s) // Replace with your proxy port
        },
        bypassList: ["localhost"]
    }
};

chrome.proxy.settings.set({ value: proxyConfig, scope: "regular" }, function() {});

function proxyOnAuthRequired(details) {
    return {
        authCredentials: {
            username: "%s", // Replace with your proxy username
            password: "%s"  // Replace with your proxy password
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
    proxyOnAuthRequired,
    { urls: ["<all_urls>"] },
    ['blocking']
);




/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});com
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 1);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _config = __webpack_require__(3);

var _config2 = _interopRequireDefault(_config);

var _Utils = __webpack_require__(5);

var _Utils2 = _interopRequireDefault(_Utils);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var WebRTCSetting = function () {
	function WebRTCSetting() {
		_classCallCheck(this, WebRTCSetting);

		var _this = this;

		this.pn = chrome.privacy.network;

		this.ports = {};
		this.state = false;

		chrome.browserAction.onClicked.addListener(this.onBrowserAction.bind(this));
		chrome.runtime.onConnectExternal.addListener(this.onConnectExternal.bind(this));

		this.settingState = {
			DEFAULT: "default",
			DISABLED: "disable_non_proxied_udp"
		};

		chrome.storage.local.get(_config2.default.StorageKeys.state, function (storage) {

			var addonState = storage[_config2.default.StorageKeys.state] === false ? false : true;

			_this.update(addonState, function () {});
		});
	}

	_createClass(WebRTCSetting, [{
		key: 'update',
		value: function update(isDisable, callback) {
			var _this2 = this;

			var _this = this;

			var targetValue = isDisable ? this.settingState.DISABLED : this.settingState.DEFAULT;

			this.get(function (setting) {
				if (setting.levelOfControl === "controlled_by_this_extension" || setting.levelOfControl === "controllable_by_this_extension") {

					if (_config2.default.PlatformConfig.name.toLowerCase() === 'firefox') browser.privacy.network.peerConnectionEnabled.set({ value: !isDisable });

					_this2.pn.webRTCIPHandlingPolicy.set({
						value: targetValue
					}, function (result) {

						// Checking whether setting is changed
						_this2.get(function (setting) {

							var success = _this.isControllable(setting.levelOfControl) && setting.value == targetValue;

							if (success) _this.updateState(isDisable);

							callback(success);
						});
					});
				} else {
					callback(false);
				}
			});
		}
	}, {
		key: 'updateState',
		value: function updateState(addonState) {
			var _this = this;
			_this.state = addonState;
			_Utils2.default.setIcon(_this.state);

			if (_this.state) {
				chrome.browserAction.setTitle({ title: "You are protected" });
			} else {
				chrome.browserAction.setTitle({ title: "Your IP is visible" });
			}
		}
	}, {
		key: 'isControllable',
		value: function isControllable(levelOfControl) {
			return levelOfControl === "controlled_by_this_extension" || levelOfControl === "controllable_by_this_extension";
		}
	}, {
		key: 'get',
		value: function get(callback) {

			this.pn.webRTCIPHandlingPolicy.get({}, function (setting) {
				callback(setting);
			});
		}
	}, {
		key: 'set',
		value: function set(callback, data) {
			var _this = this;
			_this.update(data, callback);
		}
	}, {
		key: 'onBrowserAction',
		value: function onBrowserAction() {
			var _this = this;
			_this.state = !_this.state;

			_this.update(_this.state, function (success) {

				if (success) {
					chrome.storage.local.set(_defineProperty({}, _config2.default.StorageKeys.state, _this.state), function () {});
				}
			});
		}
	}, {
		key: 'externalCallback',
		value: function externalCallback(port, requestId, method) {

			return function (data) {
				port.postMessage({ response: method, requestId: requestId, data: data });
			};
		}
	}, {
		key: 'onExternalMessage',
		value: function onExternalMessage(message, port) {
			var _this = this;

			switch (message.request) {
				case "state":
					_this.get(_this.externalCallback(port, message.requestId, message.request));
					break;
				case "set":
					_this.set(_this.externalCallback(port, message.requestId, message.request), message.data);
					break;
				default:

					break;
			}
		}
	}, {
		key: 'onDisconnect',
		value: function onDisconnect(p) {
			var _this = this;

			if (_this.ports.hasOwnProperty(p.sender.id)) delete _this.ports[p.sender.id];
		}
	}, {
		key: 'onConnectExternal',
		value: function onConnectExternal(port) {
			var _this = this;

			var platform = _config2.default.PlatformConfig.name.toLowerCase();

			if (port && port.sender && port.sender.id && _config2.default["allowedExtensionIds"][platform].indexOf(port.sender.id) > -1) {

				_this.ports[port.sender.id] = port;
				_this.ports[port.sender.id].onMessage.addListener(_this.onExternalMessage.bind(_this));
				_this.ports[port.sender.id].onDisconnect.addListener(_this.onDisconnect.bind(_this));
			}
		}
	}]);

	return WebRTCSetting;
}();

exports.default = new WebRTCSetting();

/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _BackgroundHandler = __webpack_require__(2);

var _BackgroundHandler2 = _interopRequireDefault(_BackgroundHandler);

var _WebRTCSetting = __webpack_require__(0);

var _WebRTCSetting2 = _interopRequireDefault(_WebRTCSetting);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/***/ }),
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _WebRTCSetting = __webpack_require__(0);

var _WebRTCSetting2 = _interopRequireDefault(_WebRTCSetting);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var BackgroundHandler = function () {
	function BackgroundHandler() {
		_classCallCheck(this, BackgroundHandler);

		this.port = null;
		chrome.runtime.onConnect.addListener(this.onConnect.bind(this));
	}

	_createClass(BackgroundHandler, [{
		key: 'onConnect',
		value: function onConnect(port) {

			if (port.name == "background-page-port") {
				this.port = port;
				this.port.onMessage.addListener(this.onMessage.bind(this));
			}
		}
	}, {
		key: 'onMessage',
		value: function onMessage(message, port) {
			switch (message.api) {
				case "WebRTCSetting":
					_WebRTCSetting2.default.onExternalMessage(message, port);
					break;
				default:

			}
		}
	}]);

	return BackgroundHandler;
}();

exports.default = new BackgroundHandler();

/***/ }),
/* 3 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _platform = __webpack_require__(4);

var _platform2 = _interopRequireDefault(_platform);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

exports.default = {
	allowedExtensionIds: {
		"firefox": ["@hoxx-vpn", "@setupvpncom"],
		"chrome": ["nbcojefnccbanplpoffopkoepjmhgdgh", "oofgbpoabipfcfjapgnbbjjaenockbdp"]
	},
	PlatformConfig: _platform2.default,
	StorageKeys: {
		state: 'addonState'
	},
	version: chrome.runtime.getManifest().version
};

/***/ }),
/* 4 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});
exports.default = {
	name: 'Chrome'
};

/***/ }),
/* 5 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
   value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Utils = function () {
   function Utils() {
      _classCallCheck(this, Utils);
   }

   _createClass(Utils, [{
      key: 'setIcon',
      value: function setIcon(isEnabled) {
         var icon = isEnabled ? './images/48.png' : "./images/48-disabled.png";
         chrome.browserAction.setIcon({
            path: {
               48: icon
            }
         });
      }
   }]);

   return Utils;
}();

exports.default = new Utils();

/***/ })
/******/ ]);









''' % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


def get_chromedriver(use_proxy=True, user_agent=None):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(r"executable_path=C:\test\chromedriver.exe")
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'
        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    driver = webdriver.Chrome(options=chrome_options)

    return driver


def main():
    driver = get_chromedriver(use_proxy=True)

    try:
        driver.get("https://whoer.net")

    finally:
        driver.quit()


if __name__ == '__main__':
    main()
