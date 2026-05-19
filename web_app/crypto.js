/**
 * Xử lý mã hóa AES-256-CBC và chữ ký HMAC-SHA256
 * Yêu cầu: CryptoJS
 */

const CryptoService = {
    // Phải khớp với cấu hình trong backend/security.py
    AES_KEY: CryptoJS.enc.Utf8.parse("my_aes_secret_key_32_bytes_lengt"),
    AES_IV: CryptoJS.enc.Utf8.parse("my_aes_16bytes_i"),
    HMAC_SECRET: "my_super_secret_key_32_bytes_len",

    /**
     * Mã hóa payload map thành JSON -> AES-256-CBC Base64
     */
    encryptPayload: function(payloadObj) {
        const payloadJson = JSON.stringify(payloadObj);
        
        const encrypted = CryptoJS.AES.encrypt(payloadJson, this.AES_KEY, {
            iv: this.AES_IV,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        });
        
        return encrypted.toString(); // Trả về Base64 String
    },

    /**
     * Tạo chữ ký HMAC-SHA256 cho chuỗi Base64
     */
    generateSignature: function(encryptedPayloadBase64) {
        const hash = CryptoJS.HmacSHA256(encryptedPayloadBase64, this.HMAC_SECRET);
        return hash.toString(CryptoJS.enc.Hex); // Trả về Hex string
    }
};
