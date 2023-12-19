package com.example.urnationdetector;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.Settings;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Base64;

import android.Manifest;

import org.json.JSONException;
import org.json.JSONObject;


public class MainActivity extends AppCompatActivity {
    private static final int MY_PERMISSIONS_REQUEST_WRITE_EXTERNAL_STORAGE = 1;

    ImageView imgView;
    TextView textView;
    String site_url = "https://zandhi98.pythonanywhere.com";
    JSONObject post_json;
    String imageUrl = null;
    Bitmap bmImg = null;


    CloadImage task;
    PutPost task2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        imgView = (ImageView) findViewById(R.id.imgView);
        textView = (TextView) findViewById(R.id.myTextView);
    }

    public void onClickForLoad(View v) {

        if (task != null && task.getStatus() == AsyncTask.Status.RUNNING) {
            task.cancel(true);
        }
        if (task2 != null && task2.getStatus() == AsyncTask.Status.RUNNING) {
            task2.cancel(true);
        }

        task = new CloadImage();

        task.execute(site_url + "/api_root/latest-UCF/");
        Toast.makeText(getApplicationContext(), "Load", Toast.LENGTH_LONG).show();
    }

    public void onClickForSave(View v) {

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            if (Environment.isExternalStorageManager()) {
                // 외부 저장소 관리자 권한이 이미 허용됨
                saveBitmaptoJpeg(bmImg, "DCIM", "image");
                Toast.makeText(getApplicationContext(), "Save", Toast.LENGTH_LONG).show();

            } else {
                Intent intent = new Intent(Settings.ACTION_MANAGE_ALL_FILES_ACCESS_PERMISSION);
                startActivity(intent);
            }
        } else {
            // Android 10 미만에서는 이전 방식으로 권한 요청
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, MY_PERMISSIONS_REQUEST_WRITE_EXTERNAL_STORAGE);
            }
        }

    }

    public void onClickForLabel(View v) {
        String text = ((Button) v).getText().toString();
        String label = null;
        switch (text){
            case "노상방뇨":
                label="URN";
                break;
            case "흡연":
                label="SMK";
                break;
            case "ETC":
                label="ETC";
                break;
        }

        if (task != null && task.getStatus() == AsyncTask.Status.RUNNING) {
            task.cancel(true);
        }
        if (task2 != null && task2.getStatus() == AsyncTask.Status.RUNNING) {
            task2.cancel(true);
        }

        task2 = new PutPost();
        task2.execute(label);
        Toast.makeText(getApplicationContext(), "PUT", Toast.LENGTH_LONG).show();
    }


    protected static void saveBitmaptoJpeg (Bitmap bitmap, String folder, String name){
        String ex_storage = Environment.getExternalStorageDirectory().getAbsolutePath();
        String folder_name = "/" + folder + "/";
        String file_name = name + ".jpg";
        String string_path = ex_storage + folder_name;
        Log.d("경로", string_path);

        File file_path;
        file_path = new File(string_path);

        if (!file_path.exists()) {
            file_path.mkdirs();
        }

        try {
            FileOutputStream out = new FileOutputStream(string_path + file_name);

            bitmap.compress(Bitmap.CompressFormat.JPEG, 100, out);
            out.close();

        } catch (FileNotFoundException exception) {
            Log.e("FileNotFoundException", exception.getMessage());
        } catch (IOException exception) {
            Log.e("IOException", exception.getMessage());
        }


    }

    private class CloadImage extends AsyncTask<String, Integer, Bitmap> {
        @Override
        protected Bitmap doInBackground(String... urls) {
            try {

                String apiUrl = urls[0];
                String token = "50f9df4ce578b888b76a46e57ef1d4059635b260";
                //String username = "zandhiforce";
                //String password = "";
                URL myFileUrl = new URL(apiUrl);
                HttpURLConnection conn = (HttpURLConnection) myFileUrl.openConnection();
                //String authString = username + ":" + password;
                //String authHeaderValue = "Basic " + Base64.getEncoder().encodeToString(authString.getBytes());
                conn.setRequestProperty("Authorization", "Token "+ token);
                conn.setRequestMethod("GET");
                conn.setConnectTimeout(30000);
                conn.setReadTimeout(30000);

                int responseCode = conn.getResponseCode();
                if (responseCode == HttpURLConnection.HTTP_OK) {
                    InputStream is = conn.getInputStream();
                    BufferedReader reader = new BufferedReader(new InputStreamReader(is));
                    StringBuilder result = new StringBuilder();
                    String line;
                    while ((line = reader.readLine()) != null) {
                        result.append(line);
                    }
                    is.close();

                    post_json = new JSONObject((result.toString()));

                    if (post_json.getString("title").equals("")){

                        post_json = null;
                        imageUrl = null;
                        bmImg = null;

                        return bmImg;
                    }

                    imageUrl = site_url + post_json.getString("image");
                    URL myImageUrl = new URL(imageUrl);
                    conn = (HttpURLConnection) myImageUrl.openConnection();

                    // url에서 이미지 파일가져옴
                    is = conn.getInputStream();

                    //bitmap 형식으로 변환
                    bmImg = BitmapFactory.decodeStream(is);
                }




            } catch (IOException e) {
                e.printStackTrace();
            } catch (JSONException e) {
                throw new RuntimeException(e);
            }

            return bmImg;
        }

        protected void onPostExecute(Bitmap img) {
            if (img == null) {
                textView.setText("더이상 불러올 미분류 데이터가 없습니다!");
            } else {
                imgView.setImageBitmap(bmImg);
                textView.setText("불러오기 성공! 하나의 라벨을 골라주세요!"); //post_json.toString()
            }
        }
    }

    private class PutPost extends AsyncTask<String, Void, Void> {
        @Override
        protected Void doInBackground(String... labels) {
            try {

                String token = "50f9df4ce578b888b76a46e57ef1d4059635b260";
                //String username = "zandhiforce";
                //String password = "";

                String jsonData = "{\"label\":\""+labels[0]+"\"}";

                URL url = new URL(site_url + "/api_root/latest-UCF/");
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();

                //String authString = username + ":" + password;
                //String authHeaderValue = "Basic " + Base64.getEncoder().encodeToString(authString.getBytes());
                conn.setRequestProperty("Authorization", "Token " + token);
                conn.setRequestMethod("PUT");
                conn.setRequestProperty("Content-Type", "application/json");
                conn.setDoOutput(true);

                try (OutputStream os = conn.getOutputStream()) {
                    byte[] input = jsonData.getBytes("UTF-8");
                    os.write(input, 0, input.length);
                }

                int responseCode = conn.getResponseCode();
                System.out.println("HTTP 응답 코드: " + responseCode);

                if (responseCode == HttpURLConnection.HTTP_OK) {
                    // 성공 처리 코드
                    System.out.println("PUT 요청이 성공적으로 처리되었습니다.");

                } else {
                    // 에러 처리 코드
                    System.out.println("PUT 요청이 실패하였습니다.");
                }

            } catch (IOException e) {
                e.printStackTrace();
            }

            return null;
        }
        protected void onPostExecute(Void result) {
            textView.setText("라벨링 완료! 다음 데이터를 Load 하세요!");

        }
    }
}