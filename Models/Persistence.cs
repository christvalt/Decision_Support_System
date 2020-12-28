using System;
using Microsoft.Data.Sqlite;
using System.Collections.Generic;
using SsdWebApi.Models;
using Microsoft.EntityFrameworkCore;
using System.IO;

namespace SsdWebApi
{
    public class Persistence
    {
        private readonly IndiceContext _context;

        public Persistence(IndiceContext context)
        {
            _context = context;
            //testDB();
        }

        public List<string> readIndex(string attribute) {
            List<string> serie = new List<string>();

            StreamWriter fout = new StreamWriter(attribute+".csv", false);

            serie.Add(attribute);
            fout.WriteLine(attribute);
            using (var command = _context.Database.GetDbConnection().CreateCommand())
            {
                command.CommandText = $"SELECT {attribute} FROM indici";
                _context.Database.OpenConnection();
                using (var reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        fout.WriteLine(reader[attribute]);
                        serie.Add(reader[attribute].ToString());
                    }
                }
            }
            fout.Close();
            
            return serie;
        }
        public List<string> readIndex(int id) {
            string[] indices = new string[]{"id", "Data", "SP_500", "FTSE_MIB", "GOLD_SPOT", "MSCI_EM", "MSCI_EURO", "All_Bonds", "US_Treasury"};
            return readIndex(indices[id]);
        }
            
        public void testDB()
        { 
            var connectionStringBuilder = new SqliteConnectionStringBuilder();
            //Use DB in project directory. If it does not exist, create it:
            connectionStringBuilder.DataSource = "./testDB.sqlite";
            using (var connection = new SqliteConnection(connectionStringBuilder.ConnectionString))
            { 
                connection.Open();
                //Create a table (drop if already exists):
                var delTableCmd = connection.CreateCommand();
                delTableCmd.CommandText = "DROP TABLE IF EXISTS cronistoria";
                delTableCmd.ExecuteNonQuery();
                var createTableCmd = connection.CreateCommand();
                createTableCmd.CommandText = "CREATE TABLE cronistoria(id INTEGER PRIMARY KEY, anno int, serie text)";
                createTableCmd.ExecuteNonQuery();
                //Seed some data:
                using (var transaction = connection.BeginTransaction())
                { 
                    var insertCmd = connection.CreateCommand();
                    insertCmd.CommandText = "INSERT INTO cronistoria (anno,serie) VALUES(2014,'A')";
                    insertCmd.ExecuteNonQuery();
                    insertCmd.CommandText = "INSERT INTO cronistoria (anno,serie) VALUES(2015,'B')";
                    insertCmd.ExecuteNonQuery();
                    insertCmd.CommandText = "INSERT INTO cronistoria (anno,serie) VALUES(2016,'B')";
                    insertCmd.ExecuteNonQuery();
                    insertCmd.CommandText = "INSERT INTO cronistoria (anno,serie) VALUES(2017,'B')";
                    insertCmd.ExecuteNonQuery();
                    insertCmd.CommandText = "INSERT INTO cronistoria (anno,serie) VALUES(2018,'D')";
                    insertCmd.ExecuteNonQuery();
                    transaction.Commit();
                }
                //Read the newly inserted data:
                var selectCmd = connection.CreateCommand();
                selectCmd.CommandText = "SELECT anno, serie FROM cronistoria";
                using (var reader = selectCmd.ExecuteReader())
                {
                    while (reader.Read())
                    { int anno = Convert.ToInt32(reader.GetString(0));
                    var message = anno+" "+(anno+1)+" Serie "+reader.GetString(1);
                    Console.WriteLine(message);
                    }
                }
            }
        }
    }
}