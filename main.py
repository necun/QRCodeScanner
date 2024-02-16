#press 'o' button to open the webpage

import cv2
from pyzbar.pyzbar import decode
import webbrowser

bounding_area = (230, 130, 200, 200)
qr_code_data = None


def find_qrcode_edges(image):
    return image


def scan_qr_codes(image):
    global qr_code_data
    decoded_objects = decode(image)
    if decoded_objects:
        obj = decoded_objects[0]
        bbox = obj.rect
        if (bounding_area[0] < bbox[0] < bounding_area[0] + bounding_area[2] and
                bounding_area[1] < bbox[1] < bounding_area[1] + bounding_area[3]):
            qr_code_data = obj.data.decode('utf-8')
            return True
    return False


def main():
    cap = cv2.VideoCapture(0)
    website_opened = False

    while cap.isOpened() and not website_opened:
        ret, frame = cap.read()
        if not ret:
            print("Error: Couldn't read frame")
            break


        screen_center_x = frame.shape[1] // 2
        screen_center_y = frame.shape[0] // 2

        #bounding box
        x, y, w, h = bounding_area
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        qrcode_edges = find_qrcode_edges(frame)
        cv2.imshow('QRcode Scanner', qrcode_edges)

        if scan_qr_codes(qrcode_edges):
            url_text = qr_code_data
            text_size, _ = cv2.getTextSize(url_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            text_width = text_size[0] + 20

            # coordinates for the white rectangle at the center
            rect_top_left = (screen_center_x - text_width // 2 - 10, screen_center_y - 25)
            rect_bottom_right = (screen_center_x + text_width // 2 + 10, screen_center_y + 25)

            cv2.rectangle(frame, rect_top_left, rect_bottom_right, (255, 255, 255), -1)  # white filled rectangle
            cv2.putText(frame, url_text, (screen_center_x - text_width // 2, screen_center_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)  # text in black
            cv2.imshow('QRcode Scanner', frame)

            if cv2.waitKey(0) == ord('o'):  # press 'o' to open
                webbrowser.open(qr_code_data)
                website_opened = True

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()