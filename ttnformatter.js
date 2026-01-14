function decodeUplink(input) {
  let i = 0;
  const b = input.bytes;

  let event = null;
  let temp = null;
  let def = null;

  while (i < b.length) {
    const code = b[i++];
    if (code === 0x01) {                 // event: 1 byte ASCII
      event = String.fromCharCode(b[i++]);
    } else if (code === 0x02) {          // temp: uint16 LE, /10
      const raw = b[i] + (b[i + 1] << 8);
      temp = raw / 10.0;
      i += 2;
    } else if (code === 0x03) {          // default: 1 byte
      def = b[i++];
    } else {
      return {
        data: {},
        warnings: [],
        errors: ["Unknown field code: " + code]
      };
    }
  }

  return {
    data: {
      event: event,
      temp: temp,
      default: def
    },
    warnings: [],
    errors: []
  };
}
