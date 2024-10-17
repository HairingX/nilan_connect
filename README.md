# Genvex Connect
Component to directly integrate Genvex Connect and Nilan Gateway devices into Home Assistant.
The integrationen uses a custom libary [GenvexNabto](https://github.com/HairingX/genvexnabto) which handles all communication with the devices locally. Have a look in that repo for more information about the more technical side of the project.

This integration needs the user to have an Genvex Connect or Nilan gateway connected to their device or own the newer Optima devices, which already have integrated gateways.

### Supported controller models
|Controller         | Gateway requiured     | Supported       | Tested  |
|------------------:|:---------------------:|:---------------:|:-------:|
|Optima 250         | Yes, internet gateway | ✅              |       |
|Optima 251         | Yes, internet gateway | ✅              |       |
|Optima 260         | Yes, internet gateway | ✅              |         |
|Optima 270         | Built in              | ✅              |      |
|Optima 301         | Yes, internet gateway | ✅              |      |
|Optima 312         | Yes, internet gateway | ✅              |         |
|Optima 314         | Built in              | ✅              |         |
|Nilan CTS400       | Yes, nilan gateway    | ✅              | ✅     |
|Nilan CTS602       | Yes, nilan gateway    | ✅              |      |
|Nilan CTS602 Light | Yes, nilan gateway    | ✅              |         |
|Nilan CTS602 Geo   | Yes, nilan gateway    | ✅              |         |

## Installation (HACS)

The preferred method to install is to use HACS. You need to add this repo https://github.com/HairingX/genvexconnect as a custom repo. See https://hacs.xyz/docs/faq/custom_repositories for details.

## Installation (No HACS)

If you don't have/want HACS installed, you will need to manually install the integration

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. Drag the `custom_components` folder into your HA configuration folder.
3. Restart Home Assistant

## Setup
To setup the integration, go into "Configuration" -> "Integrations" and press on the "+" button. Find Genvex Connect from the list.
The integration should search for your device and let you choose which one to use. You then need to provide it with the same email as used in the Genvex Connect app. This is case sensitive.
Then if all goes well, your device should be added and working in Home Assistant.

## Warning
Some users have posted, that Nilan have locked them out of their gateway after accessing it with other devices than their app.
I cannot confirm the validity of the posts, but to avoid getting into that situation i recommend that you

**Block all internet access for your Nilan Gateway, and only access it through the Home Assistant integration, if you choose to use that.**

## A little note to Genvex/Nilan
I know fully well that you have the ability to remotely update your devices and closing local connections are quite simple to do.
Please do not use that power irresponsibly.
The method of connecting locally does require you to know the exact email used in the app and the capabilities are the same as the ones your users connecting directly through Modbus have.
This shouldn't be a security concern and only gives your Gateway solutions much more value to the end user.

# Obligatory statement
I am not personally or in any way responsible for any damages should you choose to use the integration. No warranty provided.
Be especially observant when trying the integration with untested controller models and settings values.

## Credit
This library would not be possible without the time and effort put in by superrob, who initiated this integration.
I branched out this codebase for development practice purpose, to tailor the CTS 400 model to my needs.
For more info see his library here: https://github.com/superrob/genvexconnect
