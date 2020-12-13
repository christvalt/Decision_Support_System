using System;
using System.Drawing;
/*lavorare sugli oggetti, sull'istanza di questa classe qui*/
namespace SsdWebApi
{

    public class Forecast
    {
        public Forecast(){

        }
        public string forecastSARIMAindex(String attribute)
        {
            string res = "\"text\":\"";
            string interpreter = @"C:/Users/camerum/anaconda3/envs/open/python.exe"; 
            string environment = "open";
            int timeout = 10000;
            PythonRunner PR = new PythonRunner(interpreter,environment,timeout);
            Bitmap bmp = null;

            try
            {
                string command = $"Models/forecastStat.py {attribute}.csv";
                string list = PR.runDosCommands(command);

                if (string.IsNullOrWhiteSpace(list))
                {
                    Console.WriteLine("Error in the script call");
                    goto lend;
                }
                string[] lines = list.Split(new[] { Environment.NewLine }, StringSplitOptions.None);
                string strBitmap = "";
                foreach (string s in lines)
                {
                    if (s.StartsWith("MAPE"))
                    {
                        Console.WriteLine(s);
                        res += s;
                    }

                    if (s.StartsWith("b'"))
                    {
                        strBitmap = s.Trim();
                        break;
                    }
                    if (s.StartsWith("Actual"))
                    {
                        double fcast = Convert.ToDouble(s.Substring(s.LastIndexOf(" ")));
                        Console.WriteLine(fcast);
                    }


                }
                strBitmap=strBitmap.Substring(strBitmap.IndexOf("b'")); //begin of binary image
                res+= "\",\"img\":\""+strBitmap+"\"";
                try{
                    bmp=PR.FromPythonBase64String(strBitmap);
                }
                catch(Exception exception)
                {
                    throw new Exception(
                        "An error occuccurred while trying to create an image from Python script output. " +
                        "See inner exception for details.",
                        exception);
                    
                }
                goto lend;

            }
            catch(Exception e)
            {
                Console.WriteLine(e.ToString());
                goto lend;
            }

            lend:
            return res;
            Console.WriteLine("test"+res);
    }

    }
}