using MongoDB.Bson;
using MongoDB.Driver;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.Web;

namespace TRACE_API.Services
{
    public class MongoHelper
    {
        public IMongoCollection<BsonDocument> Collection { get; private set; }

        public MongoHelper()
        {
            var con = ConfigurationManager.ConnectionStrings["MongoDB"].ConnectionString;

            var client = new MongoClient(con);

            var db = client.GetDatabase(ConfigurationManager.AppSettings["MongoDBName"]);
            Collection = db.GetCollection<BsonDocument>(ConfigurationManager.AppSettings["MongoDBCollection"]);
        }
    }
}