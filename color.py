from __future__ import division
from xml.dom.minidom import parse


doc = parse('/Users/ashish/Library/Application Support/Sublime Text 2/Packages/Color Scheme - Default/Monokai.tmTheme')

keys = doc.getElementsByTagName('key')

ALPHA = 0

for key in keys:
    key_val = key.childNodes[0].nodeValue
    if key_val in ['foreground', 'background']:
        # Pick color if its foreground or background
        color_node = key.nextSibling.nextSibling.childNodes[0]

        # Strip '#'
        color_val = color_node.nodeValue[1:]

        # Pair 2 digit hex values for 1 channel if 6 digits color is found,
        # else 1 digit for 1 channel.
        if len(color_val) == 3:
            r, g, b = [x + x for x in list(color_val)]
        else:
            r, g, b = color_val[0:2], color_val[2:4], color_val[4:6]

        # Multiply with alpha value
        if key_val == 'foreground':
            r, g, b = [int(x, 16) * (1 + ALPHA/10) for x in r, g, b]
        else:
            r, g, b = [int(x, 16) * (1 - ALPHA/10) for x in r, g, b]


        # We don't want floats here
        r, g, b = [int(x) if x < 255 else 255 for x in r, g, b]

        # Convert into hex values.
        r, g, b = [hex(x)[2:] for x in r, g, b]

        # Convert into hex and put the '#' back
        transformed_color_val = '#' + ''.join(['0' + x if len(x) == 1 else x for x in r, g, b])

        # Writeback the transformed value into XML DOM
        color_node.nodeValue = transformed_color_val


open('/Users/ashish/Library/Application Support/Sublime Text 2/Packages/Color Scheme - Default/Experimental.tmTheme', 'w').write(
    doc.toxml().encode('utf-8'))
