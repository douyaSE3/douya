import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;


public class place_spider {
	DataBase_p db;
	Statement statement;
	public place_spider(){
		db = new DataBase_p();
		Connection conn = db.getConnection();
		try {
			statement = conn.createStatement();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	public String getContent(String url){
		HttpClient client = new DefaultHttpClient();
		String content = null;
		try{
			HttpGet httpget = new HttpGet(url);
			HttpResponse response = client.execute(httpget);
			HttpEntity entity = response.getEntity();
			content = EntityUtils.toString(entity);
		}catch(Exception e){
			e.printStackTrace();
		}finally{
			client.getConnectionManager().shutdown();
		}
		return content;
	}
	public void getInfo(String url){
		String content = getContent(url);
		String ID = "";
		String name = "";
		String hottest = "";
		String parent = "";
		String introduction = "";
		String comment = "";
		
		String regexp1 ="http://trip.douban.com/place/([0-9]+).*?";
		Pattern p1 = Pattern.compile(regexp1);
		Matcher m1 = p1.matcher(url);
		if(m1.find()){
			ID=m1.group(1);
		}
		
		String regexp2 ="<title>\\n(.*?)\\n</title>";
		Pattern p2 = Pattern.compile(regexp2);
		Matcher m2 = p2.matcher(content);
		if(m2.find()){
			name=m2.group(1);
		}
		
		String regexp3 ="<a class=\"name\" href=\"http://trip.douban.com/place/([0-9]+)/.*?place_hottest\".*?>";
		Pattern p3 = Pattern.compile(regexp3);
		Matcher m3 = p3.matcher(content);
		while(m3.find()){
			hottest+=m3.group(1);
			hottest+=" ";
		}
		
		String regexp4 ="http://trip.douban.com/place/([0-9]+)/.*?place_parent";
		Pattern p4 = Pattern.compile(regexp4);
		Matcher m4 = p4.matcher(content);
		if(m4.find()){
			parent=m4.group(1);
		}
		
		String regexp5 ="<div class=\"intro-full\" style=\"display:none;\">([\\s\\S]*)<a.*?>.*?</a></div>";
		Pattern p5 = Pattern.compile(regexp5);
		Matcher m5 = p5.matcher(content);
		if(m5.find()){
			introduction=m5.group(1);
		}else {
			String regexp5_1 ="<div class=\"intro\">(.*?)</div>";
			Pattern p5_1 = Pattern.compile(regexp5_1);
			Matcher m5_1 = p5_1.matcher(content);
			if(m5_1.find()){
				introduction = m5_1.group(1);
			}
		}
//		System.out.println(ID);
//		System.out.println(name);
//		System.out.println(hottest);
//		System.out.println(parent);
//		System.out.println(introduction);
//		System.out.println(comment);
		try {
			String s = "INSERT INTO place VALUES("+"'"+ID+"','"+name+"','"+hottest+"','"+parent+"','"+introduction.replaceAll("'", "’")+"','"+comment+"')";
			statement.executeUpdate(s);
		} catch (Exception e) {
			e.printStackTrace();
		}
		System.out.println(ID+name);
	}
	public static void main(String[] args){
		place_spider spider = new place_spider();
		for(int i=1005373;i<=1006000;i++){
			String url = "http://trip.douban.com/place/"+i+"/";
			spider.getInfo(url);
		}
	}
}
class DataBase_p {
	public static final String DRIVER="com.mysql.jdbc.Driver";
	public static final String DBURL="jdbc:mysql://localhost:3306/trip?user=root&password=admin&unicode=true&characterEncoding=UTF-8";
	
	Connection conn=null;
	
	public DataBase_p() {
		
		try{
			Class.forName(DRIVER).newInstance();
			conn=DriverManager.getConnection(DBURL);
		}catch(Exception ex){
			ex.printStackTrace();
		}
		
	}
	public Connection getConnection(){
		return conn;
	}
}
